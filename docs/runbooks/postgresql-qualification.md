# PostgreSQL scale and resilience qualification

This is the operator contract for DBM-SCALE-001, DBM-RES-001, and
DBM-QUAL-001. It can certify only this wording:

> 1,250 opaque browser identities, 250 active browser sessions, and 200
> concurrent MCP/agent clients.

It does not certify 1,250 authenticated people. Authentication, RBAC, and a
people-based claim remain separate work.

## Gate state

The repository contains the deterministic seed, stateful REST/MCP load client,
PostgreSQL evidence collector, resilience evaluator, baseline comparator, and
signed qualification assembler. Their presence is not a qualification result.
DBM-QUAL-001 passes only after an independent reviewer accepts three
consecutive, non-overlapping, complete attempts against one frozen release.

Each attempt contains seven finalized load results:

| Profile | Phase | Required duration |
| --- | --- | ---: |
| `mixed_peak_v1` | `warmup` | 15 minutes |
| `mixed_peak_v1` | `steady` | 60 minutes |
| `mixed_peak_v1` | `burst` | 10 minutes |
| `mixed_peak_v1` | `soak` | 8 hours |
| `human_peak_v1` | `steady` | 60 minutes |
| `connection_surge_v1` | `burst` | 10 minutes |
| `external_llm_wait_v1` | `external_wait` | 60 seconds |

The same attempt must also pass backend-replica loss, worker loss, writer
failover/reconnect, pool saturation, slow-query/lock, backup/PITR, and isolated
restore scenarios. Monthly 99.9% availability remains a 30-day post-release
objective, not a laboratory claim.

## Safety and prerequisites

- Run the seed only in an isolated `test` or `rehearsal` database. It refuses
  `production`, the database name `workchord`, and an authorization target
  that differs from the parsed URL.
- Qualification traffic targets `rehearsal`. Never pass the production
  authorization token merely to make a rehearsal command work.
- Use PostgreSQL 18/current supported minor with UTF-8,
  `PG_UNICODE_FAST`, UTC, schema `workchord`, and search path
  `workchord, pg_catalog`.
- Use the frozen topology: two web replicas, two delivery workers, the
  reference gateway and PostgreSQL/failover hardware, and a separate load
  generator. Record actual CPU, RAM, storage class/size/IOPS, network, and
  connection limits in sealed hardware evidence.
- Preload and install `pg_stat_statements`; enable `track_io_timing`,
  `track_wal_io_timing`, `log_lock_waits`, and the approved timeout/pool
  configuration. Do not raise pools to conceal saturation.
- Build and pin at least the backend, gateway/frontend, and PostgreSQL images
  by digest. Run the full final SQLite/PostgreSQL/installed-wheel/source-copy
  CI matrix on the same 40-character commit.
- Send raw artifacts to immutable evidence storage. The local
  `reports/qualification/database/` tree is a workspace, not the system of
  record. It must contain no database password, session token, API key, or
  qualification signing key.

Stop the attempt on a target mismatch, unsealed/tampered input, schema drift,
missing metric, reset PostgreSQL statistics, unexpected 5xx/deadlock, failed
integrity query, topology change, monitoring gap, unexplained exclusion, or
release/seed/configuration checksum change. A stopped or failed attempt
increments the attempt number and breaks the consecutive-pass sequence.

## Workspace and full seed

Create a private attempt directory and record its immutable external-storage
location in the change record:

~~~bash
export QUAL_DIR=reports/qualification/database/attempt-001
install -d -m 0700 "$QUAL_DIR"
export QUAL_DB_URL='postgresql+psycopg://<qualification-role>:<secret>@<writer-host>:5432/workchord_qualification_a'
export QUAL_DB_TARGET='<writer-host>:5432/workchord_qualification_a'
export QUAL_APP_URL='https://<rehearsal-gateway>'
export QUAL_APP_HOST='<rehearsal-gateway>'
export DEPLOYMENT_ENVIRONMENT=rehearsal
~~~

Create an Alembic-current empty database through the packaged migration job,
then seed it. `--as-of` must be a reviewed, timezone-aware timestamp near the
run so active, nearly-expired, expired, and revoked sessions have the intended
state during traffic.

~~~bash
PYTHONPATH=backend .venv/bin/python scripts/load/seed.py \
  --profile full \
  --seed 20260718 \
  --as-of '<YYYY-MM-DDTHH:MM:SS+00:00>' \
  --database-url "$QUAL_DB_URL" \
  --authorize-target "$QUAL_DB_TARGET" \
  --checkpoint "$QUAL_DIR/seed-checkpoint.json" \
  --credentials "$QUAL_DIR/seed-credentials.json" \
  --manifest "$QUAL_DIR/seed-manifest.json"
~~~

The command is resumable. A completed rerun must return identical table
cardinalities and manifest identity. The manifest must say
`qualification_eligible: true`; keep credentials mode 0600 and destroy them
after the evidence-retention handoff.

## Freeze the release

Prepare reviewed JSON bodies for hardware and CI evidence, then seal them
without overwriting the reviewed sources:

~~~bash
PYTHONPATH=backend .venv/bin/python scripts/load/seal.py \
  --input "$QUAL_DIR/hardware-reviewed.json" \
  --output "$QUAL_DIR/hardware-evidence.json"

PYTHONPATH=backend .venv/bin/python scripts/load/seal.py \
  --input "$QUAL_DIR/ci-reviewed.json" \
  --output "$QUAL_DIR/ci-evidence.json"
~~~

Hardware evidence must include `matches_reference_hardware: true` only after
the recorded topology is independently checked. CI evidence must be
`kind: workchord-ci-qualification-evidence`, `status: passed`, name the frozen
commit, and set these booleans to true: `clean_checkout`,
`postgresql_matrix`, `sqlite_lane`, `installed_wheel_postgresql`,
`source_copy_reconciliation`, `maintenance_modes`, and
`single_alembic_head`.

Freeze one release. Replace every placeholder with evidence from the release
registry; tags are insufficient.

~~~bash
PYTHONPATH=backend .venv/bin/python scripts/load/qualify.py freeze \
  --commit '<40-character-lowercase-commit>' \
  --image '<backend-image>@sha256:<64-hex>' \
  --image '<gateway-image>@sha256:<64-hex>' \
  --image 'postgres:18.4-bookworm@sha256:1961f96e6029a02c3812d7cb329a3b03a3ac2bb067058dec17b0f5596aca9296' \
  --configuration '<rendered-secret-free-deployment-manifest>' \
  --hardware-evidence "$QUAL_DIR/hardware-evidence.json" \
  --seed-manifest "$QUAL_DIR/seed-manifest.json" \
  --schema-head '<exact-alembic-head>' \
  --output "$QUAL_DIR/frozen-release.json"
~~~

Restart the three-attempt count if any frozen input changes.

## Capture one load phase

For every row in the seven-result table, capture a PostgreSQL snapshot before
traffic. Add `--include-explain` after the production-shaped seed for the
reviewed hot queries; the collector records query IDs and plans but never raw
`pg_stat_statements` query text.

~~~bash
PYTHONPATH=backend .venv/bin/python scripts/load/collect.py snapshot \
  --database-url "$QUAL_DB_URL" \
  --authorize-host '<writer-host>:5432' \
  --environment rehearsal \
  --change-id '<change-id>' \
  --label '<profile>-<phase>-before' \
  --include-explain \
  --output "$QUAL_DIR/<profile>-<phase>-before.json"
~~~

Run traffic with no duration, rate, or virtual-user overrides. An `incomplete`
client document is expected here because WAL, growth, infrastructure, and
integrity observations do not exist until after traffic. The defer flag exits
success only when those are the only missing gates.

Review both `completed_attempts` and `eligible_attempts`. The first counts
completed logical operations; the second counts every client-observed physical
attempt, including bounded connection-surge retries. SLO denominators, status
mix, RPS, latency, and operation weights use the eligible physical attempts,
so a successful retry cannot erase a failed attempt. Also review the separate
active-client, open-connection, and in-flight peaks, request/response byte
percentiles, and parsed response-cardinality percentiles.

~~~bash
PYTHONPATH=backend .venv/bin/python scripts/load/run.py \
  --profile '<profile>' \
  --phase '<phase>' \
  --base-url "$QUAL_APP_URL" \
  --authorize-host "$QUAL_APP_HOST" \
  --environment rehearsal \
  --change-id '<change-id>' \
  --credentials "$QUAL_DIR/seed-credentials.json" \
  --seed-manifest "$QUAL_DIR/seed-manifest.json" \
  --release-manifest "$QUAL_DIR/frozen-release.json" \
  --qualification-candidate \
  --defer-external-evidence \
  --run-id '<attempt-profile-phase-unique-id>' \
  --output "$QUAL_DIR/<profile>-<phase>-client.json"
~~~

Immediately capture the after snapshot:

~~~bash
PYTHONPATH=backend .venv/bin/python scripts/load/collect.py snapshot \
  --database-url "$QUAL_DB_URL" \
  --authorize-host '<writer-host>:5432' \
  --environment rehearsal \
  --change-id '<change-id>' \
  --label '<profile>-<phase>-after' \
  --include-explain \
  --output "$QUAL_DIR/<profile>-<phase>-after.json"
~~~

During the phase, export gateway, web, worker, PostgreSQL host/provider,
replication/WAL archive, and storage metrics. Seal reviewed exports with
`scripts/load/seal.py`. The eight-hour sample is the only sample from which
the collector may derive the 12-month/70% storage horizon. The attempt-wide
evidence set must provide every metric named by `evaluate_external_gates` in
`scripts/load/result.py`; missing is never zero.

After the phase and attempt-wide evidence exist, derive a document bound to
the exact client checksum. Repeat `--evidence` for the sealed application,
provider, resilience, backup/restore, and soak-horizon documents. Conflicting
values are refused. Derive the mixed eight-hour soak first and omit the
soak-horizon `--evidence` line for that command; the collector derives the
horizon from its own eight-hour snapshots. Use that sealed soak external
document as the horizon evidence for the other six results.

~~~bash
PYTHONPATH=backend .venv/bin/python scripts/load/collect.py derive \
  --before "$QUAL_DIR/<profile>-<phase>-before.json" \
  --after "$QUAL_DIR/<profile>-<phase>-after.json" \
  --load-result "$QUAL_DIR/<profile>-<phase>-client.json" \
  --phase '<phase>' \
  --evidence "$QUAL_DIR/attempt-monitoring-evidence.json" \
  --evidence "$QUAL_DIR/resilience-result.json" \
  --evidence "$QUAL_DIR/mixed_peak_v1-soak-external.json" \
  --external-output "$QUAL_DIR/<profile>-<phase>-external.json" \
  --integrity-output "$QUAL_DIR/<profile>-<phase>-integrity.json"

PYTHONPATH=backend .venv/bin/python scripts/load/finalize.py \
  --client-result "$QUAL_DIR/<profile>-<phase>-client.json" \
  --external-metrics "$QUAL_DIR/<profile>-<phase>-external.json" \
  --integrity-evidence "$QUAL_DIR/<profile>-<phase>-integrity.json" \
  --output "$QUAL_DIR/<profile>-<phase>-final.json"
~~~

The finalizer refuses evidence for another run/phase and never overwrites the
client artifact. Its exit code is zero only when every client, workload,
external, and domain-integrity gate passes.

## Resilience, query, storage, and retention evidence

Use the JSON schema in
`docs/contracts/postgresql-resilience-observations-v1.schema.json` for raw
observations. Account for every eligible client attempt during faults. Query
IDs in `explained_query_ids` must be present in the captured
`ranked_query_ids`; review actual `EXPLAIN (ANALYZE, BUFFERS, WAL, SETTINGS,
FORMAT JSON)` output before accepting tuning.

~~~bash
PYTHONPATH=backend .venv/bin/python scripts/load/seal.py \
  --input "$QUAL_DIR/resilience-observations-reviewed.json" \
  --output "$QUAL_DIR/resilience-observations.json"

PYTHONPATH=backend .venv/bin/python scripts/load/resilience.py \
  --observations "$QUAL_DIR/resilience-observations.json" \
  --output "$QUAL_DIR/resilience-result.json"
~~~

Exercise and record:

- loss of one web replica through first production-path success;
- loss/replacement of one worker through queue return to steady state;
- writer loss through unready detection, promotion, endpoint convergence,
  pool reconnect, and production-path readiness;
- pool saturation with at least 100 checkout samples;
- ordinary lock waits, deadlocks, ranked slow queries, and reviewed plans;
- WAL archive lag, replica lag, CPU, storage latency/utilization, bloat,
  analyze lag, memory growth, queue age/backlog/drain, and connection use;
- backup RPO and isolated restore RTO with zero invariant failures.

The reviewed lifecycle contract is
`docs/contracts/postgresql-data-lifecycle-policy-v1.json`. If the eight-hour
projection falls below 12 months or reaches 70% planned utilization inside 12
months, stop. Implement and test the selected expansion/archive/partition/
purge intervention before starting a new qualification attempt; the policy
document alone is not a pass.

Compare any material tuning change against its sealed baseline:

~~~bash
PYTHONPATH=backend .venv/bin/python scripts/load/compare.py \
  --baseline '<baseline-final-result.json>' \
  --tuned '<tuned-final-result.json>' \
  --change '<reviewed-change-id>' \
  --output '<comparison-report.json>'
~~~

Rerun the complete attempt and final CI matrix after any migration, index,
query, lock, pool, timeout, topology, or retention mechanism change.

## Bundle three attempts and sign

Bundle each complete attempt with exactly seven `--result` arguments, the
passing resilience result, and final CI evidence:

~~~bash
PYTHONPATH=backend .venv/bin/python scripts/load/qualify.py bundle-run \
  --run-id '<attempt-001-id>' \
  --attempt-number 1 \
  --release-manifest "$QUAL_DIR/frozen-release.json" \
  --seed-manifest "$QUAL_DIR/seed-manifest.json" \
  --result '<mixed-warmup-final.json>' \
  --result '<mixed-steady-final.json>' \
  --result '<mixed-burst-final.json>' \
  --result '<mixed-soak-final.json>' \
  --result '<human-steady-final.json>' \
  --result '<connection-burst-final.json>' \
  --result '<external-wait-final.json>' \
  --resilience "$QUAL_DIR/resilience-result.json" \
  --ci-evidence "$QUAL_DIR/ci-evidence.json" \
  --output "$QUAL_DIR/attempt-001-bundle.json"
~~~

Repeat for attempts 2 and 3. They must be unique, consecutive, non-overlapping,
and use the identical frozen-release fingerprint. Generate an Ed25519 key in
the approved signing system or, for an isolated rehearsal signer, with mode
0600. Never store it under the repository.

Finalization does not trust a bundle merely because it says `passed`. It
revalidates the exact seven unique result references, all eight required run
gates, frozen release/seed/contract identities, checksums, and timing before
signing. Verification repeats the current capacity contract and exact report
gate/evidence checks before accepting the Ed25519 signature. Freeze, bundle,
and final-report outputs refuse an existing path; never replace an earlier
attempt or signed report in place.

~~~bash
openssl genpkey -algorithm Ed25519 -out '<secure-path>/qualification-ed25519.pem'
chmod 0600 '<secure-path>/qualification-ed25519.pem'

PYTHONPATH=backend .venv/bin/python scripts/load/qualify.py finalize \
  --report-id '<approved-report-id>' \
  --release-manifest "$QUAL_DIR/frozen-release.json" \
  --run-bundle '<attempt-001-bundle.json>' \
  --run-bundle '<attempt-002-bundle.json>' \
  --run-bundle '<attempt-003-bundle.json>' \
  --signing-key '<secure-path>/qualification-ed25519.pem' \
  --signer '<independent-reviewer-name-or-id>' \
  --output '<immutable-handoff>/postgresql-precutover-qualification.json'

PYTHONPATH=backend .venv/bin/python scripts/load/qualify.py verify \
  --report '<immutable-handoff>/postgresql-precutover-qualification.json'
~~~

Independent review must verify raw manifests, checksums, exclusions, fault
timelines, invariant queries, plans, backup/restore evidence, all final CI
links, and the attestation that no intervening failed or excluded attempt was
omitted. Only then may DBM-QUAL-001 be marked complete or unblock
DBM-REHEARSE-001.
