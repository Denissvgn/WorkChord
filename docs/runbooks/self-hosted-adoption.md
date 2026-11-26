# Adopting a running instance into the self-hosted layout

This runbook moves a running WorkChord Compose project into the self-hosted
layout (`docker-compose.server.yml`, `scripts/server/`) in its own folder
outside every other project. The database and the credential sink keep their
contents. The old project stays intact until acceptance passes, so the move can
be undone.

It assumes the source is "a running compose project": a WorkChord stack started
from some source copy with its own Compose files, environment file, named
PostgreSQL volumes and a host directory that receives one-time agent keys (the
credential sink). It applies to any such project.

## Decision: copy the state, do not share volumes

The new stack gets its own **copies** of the database volume and the credential
sink. It does not declare the old volumes external.

- Rollback is trivial and complete. The old volumes are never mounted by the
  new stack, so they are exactly as they were when the old stack stopped. A
  migration that already ran only changed the copy. No database restore is
  needed to go back.
- Sharing volumes would put the old and the new project on one data directory.
  A forgotten supervisor restarting the old stack could then start a second
  PostgreSQL on a migrated data directory.
- The self-hosted acceptance script derives volume names from its own project
  name and checks them; external volumes would need a second, parallel
  definition of the layout.
- Only the database volume (hundreds of MB) and the sink (kilobytes) are
  copied. The WAL archive is not copied. A WAL archive is only useful together
  with a base backup that precedes it, so the new stack starts an empty archive
  and takes its first base backup right after acceptance (step 11). The old
  archive stays with the old project and is pruned in step 5 and removed later (step 12).

The cost is disk space for one more database copy and a short outage while
the copy runs. Both are measured in the rehearsal.

## Layout

The instance folder is a clone of the release. Everything the instance needs
lies under it, and nothing lies inside another project:

~~~text
$WORKCHORD_INSTANCE_HOME/                      a checkout of the release tag
  docker-compose.yml, docker-compose.server.yml, docker-compose.credential-sink.yml
  scripts/server/                              WorkChord's own scripts
  .runtime/autonomy/server.env                 environment file (mode 600)
  .runtime/autonomy/credential-sink/           the one credential sink (mode 700)
  .runtime/autonomy/dumps/                     database dumps (mode 700)
  .runtime/autonomy/reports/                   acceptance receipts
  .runtime/autonomy/deployment-record.json     the deployment record
~~~

The Compose project is `workchord-server`. The default instance folder is
`~/.workchord/instances/local-8480`.

## 0. Variables and helpers

Run every block in zsh or in bash 4.3 or newer (the macOS system `/bin/bash` 3.2
rejects `${OLD_FILES[-1]}`). Set these once in the shell that runs the whole procedure. The old values come
from the running project:

~~~bash
docker ps --format '{{.Names}}\t{{.Image}}\t{{.Ports}}'
docker inspect <old backend container> \
  --format '{{index .Config.Labels "com.docker.compose.project.config_files"}}'
docker inspect <old backend container> \
  --format '{{index .Config.Labels "com.docker.compose.project.working_dir"}}'
~~~

~~~bash
export WORKCHORD_INSTANCE_HOME="$HOME/.workchord/instances/local-8480"
export RELEASE_TAG=1.10.0     # release tags have no "v" prefix
export OLD_PROJECT=<old compose project name>
export OLD_SOURCE=<old working directory printed above>
export OLD_ENV=<environment file the old stack was started with>
export OLD_SINK=<host directory the old backend mounts as its credential sink>
OLD_FILES=(-f <old compose file> -f <next old compose file> ...)   # in the printed order
export NEW_PROJECT=workchord-server
export NEW_SINK="$WORKCHORD_INSTANCE_HOME/.runtime/autonomy/credential-sink"
export DUMPS="$WORKCHORD_INSTANCE_HOME/.runtime/autonomy/dumps"

old_compose() { docker compose --project-name "$OLD_PROJECT" --env-file "$OLD_ENV" "${OLD_FILES[@]}" "$@"; }
new_compose() {
  (cd "$WORKCHORD_INSTANCE_HOME" && docker compose --project-name "$NEW_PROJECT" \
    --env-file .runtime/autonomy/server.env \
    -f docker-compose.yml -f docker-compose.server.yml -f docker-compose.credential-sink.yml \
    --profile autonomy "$@")
}
~~~

Never print the environment files. Commands below read secrets only inside
the command that needs them.

## 1. Preconditions

Do not start the window until every item holds:

1. The release tag exists, and its release notes name the migration.
2. Port and disk: the instance's HTTP and PostgreSQL host ports are the ones
   the old stack uses today (it is stopped before the new stack starts), and
   the Docker host has free space for one more database volume plus images
   (`docker system df`).
3. **Supervisors.** Anything that restarts the old stack when its health check
   fails (a launchd agent, a systemd unit, a cron job) is identified. It will
   be unloaded in step 7, otherwise it fights the cutover.
4. **Readers of the sink.** Every service that reads agent keys from the old
   sink path is identified. After the cutover, new keys are written to the new
   sink, so each reader must be unloaded or repointed (step 10). Plan this
   before the window.
5. The maintenance window procedure is ready: follow
   [Coordinated maintenance window](control-plane-maintenance-window.md) steps
   1 to 5. Concretely: no running run and no live claim (or every live claim
   acknowledged by its owner), and **every PM has a notice receipt**. The
   `max_outage_seconds` you announce comes from the rehearsal below. If you
   have not measured it, do not guess.

## 2. Install the release folder

~~~bash
mkdir -p "$(dirname "$WORKCHORD_INSTANCE_HOME")"
git clone https://github.com/Denissvgn/WorkChord.git "$WORKCHORD_INSTANCE_HOME"
git -C "$WORKCHORD_INSTANCE_HOME" rev-parse --verify --quiet "refs/tags/$RELEASE_TAG"   # must print a commit
git -C "$WORKCHORD_INSTANCE_HOME" checkout "$RELEASE_TAG"
git -C "$WORKCHORD_INSTANCE_HOME" status --porcelain      # must print nothing
git -C "$WORKCHORD_INSTANCE_HOME" rev-parse HEAD          # the source revision
~~~

The acceptance script refuses a dirty checkout, and its images are tagged with
this revision. Do not edit files in the folder.

## 3. Seed the environment file

The self-hosted layout adds separate PostgreSQL identities and acceptance
services. The existing database and settings need the secrets they were created
with. The seed script copies exactly those from the old environment file and
generates the new ones. It never prints a value and refuses to overwrite a file:

~~~bash
mkdir -p -m 700 "$WORKCHORD_INSTANCE_HOME/.runtime/autonomy" "$DUMPS"
python3 "$WORKCHORD_INSTANCE_HOME/scripts/server/seed_adoption_env.py" \
  --old-env "$OLD_ENV" \
  --output "$WORKCHORD_INSTANCE_HOME/.runtime/autonomy/server.env" \
  --http-port 8480 --postgres-port 55432 \
  --set 'MCP_ALLOWED_HOSTS=["localhost","127.0.0.1","localhost:*","127.0.0.1:*","[::1]:*"]' \
  --set AGENT_LAST_SEEN_INTERVAL_SECONDS=60
~~~

Use the ports of the old stack. The two `--set` values keep behavior a client
of the old stack may rely on; drop what you do not need. Session cookies are
not marked `Secure` unless you pass `--session-cookie-secure`; mark them when
a TLS reverse proxy fronts the instance. The script also copies, when set:
`WORKCHORD_AUTH_MODE`, `MODEL_AWARE_ROUTING_MODE`, `CORS_ORIGINS`,
`AGENT_TEAM_CREDENTIAL_SINK_REF`, `AGENT_SKILL_BUNDLES_PUBLIC` and
`AGENT_SKILL_BUNDLE_TRUSTED_CHECKSUMS_SHA256`. Settings of the old file that
WorkChord's Compose files do not read are not copied.

Back up the new `server.env` outside the host. The acceptance script refuses
to run against an existing database without it.

An instance already in this layout keeps its `server.env` across releases. A
file written before the acceptance evidence store moved from MinIO to the
Versity S3 Gateway still names `MINIO_*` and `AUTONOMY_MINIO_*` settings and
lacks `WORKCHORD_READINESS_DETAIL_TOKEN`. The acceptance script replaces and
adds them on its next run. Before running Docker Compose
by hand against such a file, migrate it in place:

~~~bash
python3 "$WORKCHORD_INSTANCE_HOME/scripts/server/seed_adoption_env.py" \
  --migrate-env "$WORKCHORD_INSTANCE_HOME/.runtime/autonomy/server.env"
~~~

The [acceptance runbook](self-hosted-server-acceptance.md#evidence-store)
describes the new settings, the readiness detail token and the old evidence
volume.

## 4. Isolated rehearsal on a restored copy

The rehearsal runs the release's migration on a restored copy of the live
database in a separate Compose project with its own ports and volumes. It
measures the migration and repair, including the project identity scan, which
is the longest step on a large history. The old stack keeps running.

~~~bash
export REH_PROJECT=workchord-adoption-rehearsal
export REH_HOME="$HOME/.workchord/rehearsal"
mkdir -p -m 700 "$REH_HOME/reports"
python3 "$WORKCHORD_INSTANCE_HOME/scripts/server/seed_adoption_env.py" \
  --old-env "$OLD_ENV" --output "$REH_HOME/server.env" \
  --http-port 18480 --postgres-port 55492
printf '%s\n' "WORKCHORD_IMAGE_PREFIX=$REH_PROJECT" \
  "WORKCHORD_SOURCE_REVISION=$(git -C "$WORKCHORD_INSTANCE_HOME" rev-parse HEAD)" \
  "WORKCHORD_ACCEPTANCE_REPORT_DIR=$REH_HOME/reports" >>"$REH_HOME/server.env"
reh() {
  (cd "$WORKCHORD_INSTANCE_HOME" && docker compose --project-name "$REH_PROJECT" \
    --env-file "$REH_HOME/server.env" -f docker-compose.yml -f docker-compose.server.yml \
    --profile autonomy "$@")
}

# A logical dump of the live database (read-only on the live stack).
DUMP="$DUMPS/rehearsal-$(date -u +%Y%m%dT%H%M%SZ).dump"
docker exec "${OLD_PROJECT}-postgres-1" pg_dump -U postgres -Fc workchord >"$DUMP"
( cd "$DUMPS" && shasum -a 256 "$(basename "$DUMP")" | tee "$(basename "$DUMP").sha256" )

reh build backend frontend
reh up --detach --wait postgres
# The rehearsal database is disposable, so --clean is acceptable here and only here.
reh exec -T postgres pg_restore -U postgres -d workchord --clean --if-exists --no-owner <"$DUMP"
reh run --rm --no-deps database-bootstrap
time reh run --rm --no-deps migration python -m app.cli.upgrade --no-repairs \
  --external-backup-reference "rehearsal-$(basename "$DUMP")"
reh run --rm --no-deps database-security
time reh run --rm --no-deps repair
~~~

The two `time` results are the database part of the outage. A refusal such as
`project_history_scan_limit` means the release does not support this database
as it stands: stop, keep the old stack, and report it. Do not patch the
release for the cutover.

Then start the application on the restored copy and read it:

~~~bash
reh up --detach --wait --no-deps backend frontend
reh exec -T backend python -c "import urllib.request; print(urllib.request.urlopen('http://localhost:8001/health/ready').read().decode())"
curl -fsS http://127.0.0.1:18480/health
~~~

Readiness is not exposed through the web port: the frontend answers 404 for
`/health/ready`. Read it from inside the backend container, as above. The
`/health` check through the port is liveness only.

Add the timings to the rest of the window budget (stop, copy, startup,
acceptance; step 9 gives the commands you can time) and a margin, and use the
sum as `max_outage_seconds`. Remove the rehearsal when done:

~~~bash
reh down --volumes --remove-orphans
docker image ls --format '{{.Repository}}:{{.Tag}}' | grep "^$REH_PROJECT-" | xargs -r docker image rm
rm -rf "$REH_HOME"
~~~

## 5. Fresh verified base backup and the WAL prune dry run

Run this on the old project, shortly before the window, while it still serves.

~~~bash
export PG_IMAGE="$(sed -n 's/^    image: \(postgres:[^ ]*\)$/\1/p' "$WORKCHORD_INSTANCE_HOME/docker-compose.yml" | head -1)"
# A shell variable wins over the env file, and Compose reads it when it parses
# the file, so it reaches the job's DATABASE_BACKUP_URL (`run -e` would not).
POSTGRES_BACKUP_URL="postgresql://postgres:$(sed -n 's/^POSTGRES_PASSWORD=//p' "$OLD_ENV")@postgres:5432/workchord" \
  old_compose --profile backup run --rm --no-deps base-backup
docker run --rm -v "${OLD_PROJECT}_workchord_postgresql_backups:/backups:ro" "$PG_IMAGE" \
  sh -c 'ls -1 /backups/base | tail -3; for d in /backups/base/workchord-*; do test -f "$d/backup_label" -a -f "$d/workchord-files.sha256" && echo "verified: $d"; done | tail -1'
~~~

If the old Compose file has no `base-backup` service, run the same job from
the release with the old project name and the old data volume mounted
read-only, or take the backup as the
[backup runbook](postgresql-backup-restore.md) describes. A backup counts only
once its final `workchord-<timestamp>` directory holds `backup_label` and
`workchord-files.sha256`. Record that directory name:

~~~bash
export BACKUP_REFERENCE="base-backup:${OLD_PROJECT}:<the verified workchord-<timestamp> name>"
~~~

Now size the old archive and preview the prune. The same helper serves the old
and the new project name:

~~~bash
prune_wal() {   # prune_wal <project> [--dry-run]
  project="$1"; shift
  docker run --rm \
    -v "${project}_workchord_postgresql_wal_archive:/var/lib/postgresql/wal-archive" \
    -v "${project}_workchord_postgresql_backups:/backups:ro" \
    -v "$WORKCHORD_INSTANCE_HOME/scripts/database_backup/prune_wal_archive.sh:/opt/workchord/prune_wal_archive.sh:ro" \
    "$PG_IMAGE" /bin/bash /opt/workchord/prune_wal_archive.sh "$@"
}
docker run --rm -v "${OLD_PROJECT}_workchord_postgresql_wal_archive:/a:ro" "$PG_IMAGE" du -sh /a
prune_wal "$OLD_PROJECT" --dry-run
~~~

Exit status 3 right after a fresh backup only means its start segment is not
archived yet: switch the segment and repeat the dry run:

~~~bash
old_compose exec -T postgres psql -U postgres -d workchord -Atc 'SELECT pg_switch_wal()'
sleep 10
prune_wal "$OLD_PROJECT" --dry-run
~~~

When the dry run is clean, prune for real:

~~~bash
prune_wal "$OLD_PROJECT"
~~~

This is safe now. It keeps every segment from the start of the backup you just
verified. Rollback A and B start the old PostgreSQL on its untouched data
volume and never read the archive. Rollback C restores from this backup and
replays only later segments, which are kept. No earlier base backup exists, so
the removed segments cannot recover anything.

## Before the window: pending deliveries

The new stack runs the outbound delivery worker, which the old instance may not
have been running. Pending deliveries would be sent the moment it
starts. The table holds webhook, email and inbox delivery rows. Look first, read-only:

~~~bash
old_compose exec -T postgres psql -U postgres -d workchord -c \
  "select status, count(*), min(created_at) from outbound_webhook_deliveries group by status"
~~~

If `pending` is not zero, ask the owner whether those deliveries may go out.
There is no supported way to discard pending deliveries. If the owner does not
want them sent, do not start the window; report it. Do not edit the table by
hand.

## 6. Announce the window

Follow steps 2 to 5 of the
[maintenance window runbook](control-plane-maintenance-window.md) with
`release_label` set to the release and the `max_outage_seconds` from step 4.
Wait until `readiness.blockers` is empty and every PM has a notice receipt.

## 7. Begin, drain, stop the old stack

Begin the window and drain writes as steps 6 of that runbook describes. Then
stop the supervisors from step 1.3 first. Examples:

~~~bash
launchctl bootout "gui/$(id -u)/<supervisor label>"     # launchd
systemctl --user disable --now <supervisor unit>         # systemd
~~~

While the old stack is still up and drained, record its row counts:

~~~bash
COUNTS="select table_name, (xpath('/row/c/text()', query_to_xml(format('select count(*) as c from workchord.%I', table_name), false, true, '')))[1]::text from information_schema.tables where table_schema='workchord' and table_type='BASE TABLE' order by 1"
old_compose exec -T postgres psql -U postgres -d workchord -Atc "$COUNTS" >"$DUMPS/counts-old.txt"
# Save the old backend's build identity now; after step 9 that port serves the new stack.
curl -fsS http://127.0.0.1:8480/.well-known/workchord-build.json >"$DUMPS/previous-build.json"
python3 -c 'import json,sys; print("old source_revision:", json.load(open(sys.argv[1]))["source_revision"])' "$DUMPS/previous-build.json"
~~~

Stop the old stack. Stop is not `down`: containers and volumes stay.

~~~bash
old_compose stop --timeout 60
docker run --rm -v "${OLD_PROJECT}_workchord_postgresql18_data:/var/lib/postgresql:ro" \
  "$PG_IMAGE" sh -c 'pg_controldata /var/lib/postgresql/18/docker | grep "cluster state"'
~~~

The state must read `shut down`. If it does not, start the old stack again
(`old_compose start`) and investigate; never copy a volume of a running or
crashed cluster.

## 8. Copy the database volume and the sink

~~~bash
OLD_DATA="${OLD_PROJECT}_workchord_postgresql18_data"
NEW_DATA="${NEW_PROJECT}_workchord_postgresql18_data"
set -e   # fail fast: a failed check below must stop the block
if docker volume inspect "$NEW_DATA" >/dev/null 2>&1; then echo "STOP: $NEW_DATA already exists"; false; fi
docker volume create \
  --label "com.docker.compose.project=$NEW_PROJECT" \
  --label com.docker.compose.volume=workchord_postgresql18_data "$NEW_DATA"
docker run --rm --entrypoint /bin/sh -v "$OLD_DATA:/from:ro" -v "$NEW_DATA:/to" \
  "$PG_IMAGE" -c 'cd /from && cp -a . /to/'

volume_digest() {
  docker run --rm --entrypoint /bin/sh -v "$1:/v:ro" "$PG_IMAGE" -c \
    'cd /v && find . -type f -print0 | sort -z | xargs -0 sha256sum | sha256sum;
     find . -printf "%p %U:%G %m\n" | sort | sha256sum'
}
diff <(volume_digest "$OLD_DATA") <(volume_digest "$NEW_DATA")
echo "database volume copy identical"

mkdir -p -m 700 "$NEW_SINK"
cp -Rp "$OLD_SINK/." "$NEW_SINK/"
diff -r "$OLD_SINK" "$NEW_SINK"
echo "sink identical"
ls "$NEW_SINK" | wc -l
set +e
~~~

Paste the block into a shell you can restart: with `set -e` a failed check ends
the shell, which is the point. Run `set +e` again in a new shell if it did.

If a digest differs or the sink differs, do not continue: remove the copy
(`docker volume rm "$NEW_DATA"`, and `rm -rf "$NEW_SINK"` after listing it),
restart the old stack with `old_compose start`, and complete the window as
`rolled_back`.

## 9. Bring up the release and run acceptance

~~~bash
cd "$WORKCHORD_INSTANCE_HOME"
time env \
  WORKCHORD_CREDENTIAL_SINK_HOST_DIR="$NEW_SINK" \
  WORKCHORD_MIGRATION_BACKUP_REFERENCE="$BACKUP_REFERENCE" \
  ./scripts/server/accept_self_hosted.sh
~~~

The script builds the images from the clean checkout, starts PostgreSQL on the
copied data, creates the separate PostgreSQL identities, runs the migration with
your backup reference as its recovery point, applies the database security
step, runs the repair job, starts the application and runs acceptance. It
writes the receipt to `.runtime/autonomy/reports/latest.json`. It needs no
other input: the environment file is already complete, so it rotates nothing.

Check the result:

~~~bash
new_compose exec -T backend python -c "import urllib.request; print(urllib.request.urlopen('http://localhost:8001/health/ready').read().decode())"
curl -fsS http://127.0.0.1:8480/health
new_compose ps --all
~~~

Compare table row counts with the ones recorded in step 7. Tables that existed
before must keep at least their old row count; a difference beyond seeded rows
is a stop:

~~~bash
new_compose exec -T postgres psql -U postgres -d workchord -Atc "$COUNTS" >"$DUMPS/counts-new.txt"
diff "$DUMPS/counts-old.txt" "$DUMPS/counts-new.txt"
ls "$NEW_SINK" | wc -l
~~~

## 10. Write the deployment record, hand over, close the window

~~~bash
# The revision the old images were built from. Read it from the old release
# file when it names one (the source copy's own HEAD can be older than the
# pinned images). If the header is missing, set OLD_REVISION by hand from
# source_revision in $DUMPS/previous-build.json (saved in step 7), not from
# port 8480, which serves the new stack by now.
OLD_REVISION="$(sed -n 's/^# WorkChord main \([0-9a-f]\{7,40\}\).*/\1/p' "${OLD_FILES[-1]}" | head -1)"
# If empty, the old revision is not in this repository's history; set OLD_VERSION by hand from that revision's backend/pyproject.toml.
OLD_VERSION="$(git -C "$WORKCHORD_INSTANCE_HOME" show "$OLD_REVISION:backend/pyproject.toml" 2>/dev/null | sed -n 's/^version = "\(.*\)"/\1/p')"
echo "replaces revision=${OLD_REVISION:?set OLD_REVISION by hand} version=${OLD_VERSION:-unknown}"
python3 scripts/server/write_deployment_record.py \
  --folder "$WORKCHORD_INSTANCE_HOME" --operator "$USER" \
  --replaces-project "$OLD_PROJECT" \
  --compose-file docker-compose.yml --compose-file docker-compose.server.yml \
  --compose-file docker-compose.credential-sink.yml \
  --replaces-revision "$OLD_REVISION" --replaces-version "$OLD_VERSION"
cat .runtime/autonomy/deployment-record.json
~~~

The record names, for every service, the image reference, the immutable image
ID and any registry digest; the source revision, tag and whether the checkout
is clean; the WorkChord version; the Compose project and folder; the database
volume names; the credential sink path; the time and operator; and the
deployment it replaces (its project, source revision, version, images and
volumes). It holds no secrets. Images built from the checkout have an image ID
but no registry digest. Start any scratch twin from the image IDs in this
record. Writing a record again archives the previous one under
`.runtime/autonomy/deployments/`.

Then:

1. Point every reader of the sink at `$NEW_SINK` (or start it from
   `WORKCHORD_INSTANCE_HOME`) and keep the old supervisors unloaded.
2. Confirm a run owner can renew a claim and a PM can read its team.
3. Complete the window (`"outcome": "completed"`), as step 8 of the
   maintenance runbook describes.

## 11. First base backup of the new stack

The new archive starts empty, so point-in-time recovery begins with a base
backup of the new stack. Take it before the end of the day:

~~~bash
new_compose --profile backup run --rm base-backup
prune_wal "$NEW_PROJECT" --dry-run
~~~

The retention service in `docker-compose.yml` prunes the new archive every six
hours from then on.

## 12. Retire the old project

Keep the old project untouched until the new stack has run long enough that
you no longer want the option to go back (agree the period with the team).

The old archive was pruned in step 5. When the owner approves removing the old
project, list and then remove its resources. This is permanent:

~~~bash
old_compose down --remove-orphans
docker volume ls --filter "label=com.docker.compose.project=$OLD_PROJECT"
# only after reading the list, and only these volumes:
docker volume rm "${OLD_PROJECT}_workchord_postgresql18_data" \
  "${OLD_PROJECT}_workchord_postgresql_wal_archive" "${OLD_PROJECT}_workchord_postgresql_backups"
~~~

Keep the old base backup, or copy it off the host, until the new stack has a
verified base backup of its own and a tested restore.

## Rollback

Decide by the clock: the old stack holds the data as of step 7. Everything the
new stack recorded since (claims, runs, new agent keys) is not in it. Treat
each claim by its recorded resumption state and recover lost claims through the
PM, as the maintenance runbook describes.

### A. The old volumes are intact (before step 12 removes them)

~~~bash
new_compose down                       # keeps the new volumes for inspection
old_compose up --detach --no-build backend frontend   # the pinned images, original volumes
old_compose exec -T backend python -c "import urllib.request; print(urllib.request.urlopen('http://localhost:8001/health/ready').read().decode())"
curl -fsS http://127.0.0.1:8480/health
~~~

The old stack starts against the original volume and sink, at the old schema
and old images. No database restore is needed, even if the migration in step 9
already ran: it ran on the copy. Then:

1. Load the old supervisors and readers again with their old paths.
2. Do not copy keys from the new sink back. Keys issued after the cutover
   refer to rows the old database does not have; revoke and reissue them.
3. Complete the window with `"outcome": "rolled_back"`.
4. Keep the new volumes until you know why it failed. To remove only the
   copies: `new_compose down --volumes`, after reading the volume names it
   will print with `docker volume ls --filter label=com.docker.compose.project=$NEW_PROJECT`.

### B. A failure inside the window, before acceptance passed

The same commands as A apply. The old data volume was only read, so
`old_compose up --detach --no-build backend frontend` is enough.

### C. The old data volume is gone or was modified

Restore from the verified base backup or the dump of step 4, as the
[backup runbook](postgresql-backup-restore.md) describes: create an empty
volume under the old project name, copy the backup directory into it with
`recovery.signal` and `restore_command`, start only the old PostgreSQL, check
the data, then start the old stack. A restore discards every write after its
recovery point, including claim renewals, and recovery is forward-only.

## Limits

- The new stack runs the self-hosted acceptance profile. Its signer, object
  store and CAS services are analogues, as
  [the acceptance runbook](self-hosted-server-acceptance.md) states.
- The procedure moves PostgreSQL, the credential sink and the settings in the
  environment file. It does not move host-level configuration of other
  services that talk to the instance.
