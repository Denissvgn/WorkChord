# PostgreSQL post-cutover release and closeout

This DBM-DOC-002/DBM-CLOSE-001 runbook begins only after the signed
DBM-CUT-002 production record exists. The installed `workchord-db-closeout`
command verifies and records evidence only. It never connects to a database,
changes a deployment, edits an existing document, disposes of SQLite, or grants
production authorization.

The repository currently supplies the implementation and contract, not a
production-cutover claim. Missing production evidence produces `NO-SHIP`.
A local test, synthetic signed chain, generated Markdown file, or author review
cannot complete either task.

## Trust, storage, and signer separation

Run the command from the exact installed backend wheel and record its wheel
SHA-256 plus:

~~~bash
.venv/bin/workchord-db-closeout --help
.venv/bin/workchord-db-closeout publish-release --help
.venv/bin/workchord-db-closeout finalize-closeout --help
.venv/bin/workchord-db-closeout verify --help
~~~

Provision distinct Ed25519 keys for the post-cutover publication owner and the
independent closure auditor. Supply every trusted public key from the approved
trust store; an embedded key cannot trust itself. Private keys remain outside
the repository and evidence workspace with mode `0600`. If encrypted, the
command uses `WORKCHORD_CUTOVER_SIGNING_PASSWORD` without recording it.

All generated JSON is checksummed, signed, mode `0600`, and never overwritten.
Rendered release notes are mode `0644` and also never overwritten. Transfer the
JSON, Markdown, source evidence, public keys, and checksums to the immutable
change/evidence store. The local `reports/qualification/database/` path is only
a workspace.

Inputs and output must contain no password, token, cookie, API key, private key,
database URL, DSN, authorization header, credential-bearing URL, private
hostname, private address, or production target identity. Artifact links use a
public HTTPS URL without query credentials or a stable secret-free URN.

## DBM-DOC-002 — publish actual release facts

Do not draft production facts from the intended topology. Start with all of the
following trusted artifacts for the same frozen release:

- frozen release manifest and exact installed application package;
- signed DBM-QUAL-001 report containing the final three consecutive complete
  attempts and its independently provisioned public key;
- signed DBM-CUT-002 production record and its independently provisioned public
  key;
- the released README, database policies, deployment, security, backup,
  qualification, migration, cutover, troubleshooting, and this closeout
  runbook.

The publication command revalidates the complete qualification and production
records, release fingerprint, commit, digest-pinned images, capacity contract,
schema head, current document checksums, installed package version, source
`pyproject.toml` version, and FastAPI version. A changed document, version
mismatch, stale evidence checksum, nonpublic artifact link, or expired
exception is a refusal.

Create a reviewed JSON input matching the packaged
[post-cutover publication input schema](../../backend/app/database_migration/postgresql-postcutover-publication-input-v1.schema.json)
and exactly this shape:

~~~json
{
  "kind": "workchord-postgresql-postcutover-publication-input",
  "schema_version": 1,
  "publication_id": "workchord-postgresql-release-1.6.2",
  "published_at": "2026-08-01T12:00:00+00:00",
  "status": "approved_for_publication",
  "application_version": "1.6.2",
  "postgresql_version": "18.4",
  "postgresql_version_evidence_sha256": "<sha256>",
  "release_boundary": "workchord-1.6.2",
  "artifact_references": [
    {
      "kind": "precutover_qualification",
      "public_uri": "urn:workchord:evidence:qualification:<id>",
      "sha256": "<trusted-report-sha256>"
    },
    {
      "kind": "production_cutover",
      "public_uri": "urn:workchord:evidence:cutover:<change-id>",
      "sha256": "<trusted-report-sha256>"
    }
  ],
  "operational_exceptions": [],
  "approval": {
    "product_owner": "<named-product-owner>",
    "release_owner": "<post-cutover publication owner and signer>",
    "evidence_sha256": "<approval-sha256>"
  }
}
~~~

Every approved operational exception has `id`, public `summary`, `owner`,
`approved_at`, future `expires_at`, and `approval_evidence_sha256`. Do not put a
private incident description or topology in the summary.

Sign the canonical publication:

~~~bash
.venv/bin/workchord-db-closeout publish-release \
  --input '<reviewed>/postcutover-publication-input.json' \
  --repository-root '<released-source-root>' \
  --release-manifest '<immutable>/frozen-release.json' \
  --qualification-report '<immutable>/postgresql-precutover-qualification.json' \
  --qualification-public-key '<trust-store>/qualification-ed25519-public.pem' \
  --production-cutover '<immutable>/production-cutover.signed.json' \
  --production-public-key '<trust-store>/production-record-ed25519-public.pem' \
  --signing-key '<signer>/publication-ed25519-private.pem' \
  --signer '<post-cutover publication owner>' \
  --output '<immutable-handoff>/postcutover-publication.signed.json'

.venv/bin/workchord-db-closeout verify \
  --report '<immutable-handoff>/postcutover-publication.signed.json' \
  --trusted-public-key '<trust-store>/publication-ed25519-public.pem'
~~~

The signed document contains deterministic Markdown with:

- actual WorkChord, PostgreSQL, schema, commit, and release-boundary versions;
- PostgreSQL as the sole writable production system of record;
- SQLite production support removed at that boundary while direct development,
  test, and frozen read-only migration-source use remains explicit;
- the exact **1,250 opaque browser identities, 250 active browser sessions, and
  200 concurrent MCP/agent clients** capacity boundary and its frozen workload,
  data, configuration, image, and hardware context;
- an explicit statement that this does not certify 1,250 authenticated people;
- public or opaque qualification and cutover references;
- forward-only PostgreSQL recovery and approved operational exceptions;
- the monthly 99.9% objective as pending until the complete 30-day SLI window.

Render that exact signed content once, then publish it through the release
system without hand editing:

~~~bash
.venv/bin/workchord-db-closeout render-release-notes \
  --publication '<immutable>/postcutover-publication.signed.json' \
  --publication-public-key '<trust-store>/publication-ed25519-public.pem' \
  --output '<release-handoff>/postgresql-production-transition.md'
~~~

The rendered SHA-256 must equal `release_notes.sha256` in the signed
publication. A second output at the same path is refused. DBM-DOC-002 is
complete only after the signed JSON, rendered document, release-system record,
secret scan, and stale-SQLite-instruction scan are independently reviewed.

## Stabilization observations for DBM-CLOSE-001

Start the availability clock at the `stabilization_started_at` value embedded
in the trusted production cutover. PostgreSQL remains the only writer. Keep the
frozen source snapshot read-only through its approved retention date.

The independent audit collects:

1. the approved stabilization duration, approval checksum, exact start/end,
   and evidence index;
2. one controlled post-cutover production-path verification profile with all
   applicable SLOs passing and zero unexplained integrity differences;
3. a fresh post-cutover backup plus isolated restore at the released Alembic
   head, RPO at most five minutes, RTO at most 30 minutes, and reconciliation;
4. separate evidence for application logs, unexpected errors, slow queries,
   lock waits/deadlocks, pool pressure, worker queues, and domain integrity;
5. the SQLite snapshot checksum, read-only state, retention approval, retention
   date, and eventual disposal evidence;
6. the client/gateway availability denominator beginning at cutover.

The 99.9% availability field has four states. `not_started` is valid only
before production cutover. `pending` contains no completed counts, evidence, or
claim and is allowed only before 30 complete days. `met` requires at least 30
consecutive days, a complete eligible-attempt denominator, arithmetic at or
above 99.9%, and `objective_claimed: true`. `missed` records the complete
denominator with `objective_claimed: false` and blocks SHIP. A pending window
that reaches 30 days without complete evidence also blocks SHIP.

The availability objective is not a reason to hide preliminary failures. Every
eligible DNS, TLS, gateway, timeout, reset, refusal, application, and database
attempt remains in the denominator according to the capacity contract.

## Task, gate, exception, and observation input

Create one `workchord-postgresql-closeout-observations` JSON object matching
the packaged
[closeout observations schema](../../backend/app/database_migration/postgresql-closeout-observations-v1.schema.json)
at schema version `1`. It must contain every DBM task from `DBM-CON-001` through
`DBM-DOC-002` exactly once. `DBM-CLOSE-001` is represented by the signed
decision itself. It must also contain release gates `G1` through `G15` and all
seven operational audit checks.

Each task entry has exactly `status`, `evidence_sha256`, and `exception_id`:

- `complete` requires evidence and no exception;
- `waived` requires evidence and a referenced, approved, unexpired waiver;
- `incomplete` requires a referenced exception with an owner and expiry and
  always blocks SHIP.

Each gate uses the same fields with `passed`, `waived`, `failed`, or `pending`.
DBM-QUAL-001/G10, DBM-CUT-002/G13, and DBM-DOC-002/G15 must bind the exact
trusted report checksums. DBM-QUAL-001, DBM-CUT-002, DBM-DOC-002, and gates
G10, G13, G14, G15 are non-waivable. G14 cannot pass unless stabilization,
post-cutover verification, restore, operational audit, availability timing,
and SQLite retention are internally consistent.

Every exception has exactly `id`, `status`, `owner`, `expires_at`, `scope`,
`rationale`, and `approval_evidence_sha256`. `approved_waiver` requires an
approval checksum. `open` remains a blocker. Expired, unreferenced, out-of-
scope, or missing exceptions are refused or block the verdict; none silently
becomes complete.

The input also carries the exact no-omission text printed by the tool contract
as `no_omission_attestation` and one immutable `evidence_index_sha256`. Use the
runtime validator as the semantic authority for timestamp order, task/gate
sets, RPO/RTO, availability arithmetic, retention, and dependency identity.

## Issue the independent decision

For an eligible SHIP audit, pass every dependency and trusted key:

~~~bash
.venv/bin/workchord-db-closeout finalize-closeout \
  --input '<independent-review>/closeout-observations.json' \
  --repository-root '<released-source-root>' \
  --release-manifest '<immutable>/frozen-release.json' \
  --qualification-report '<immutable>/postgresql-precutover-qualification.json' \
  --qualification-public-key '<trust-store>/qualification-ed25519-public.pem' \
  --production-cutover '<immutable>/production-cutover.signed.json' \
  --production-public-key '<trust-store>/production-record-ed25519-public.pem' \
  --publication '<immutable>/postcutover-publication.signed.json' \
  --publication-public-key '<trust-store>/publication-ed25519-public.pem' \
  --signing-key '<independent-auditor>/closure-ed25519-private.pem' \
  --signer '<same identity named as independent auditor in the input>' \
  --output '<immutable-handoff>/postgresql-closure-decision.signed.json'
~~~

The command does not accept a requested verdict. It derives `SHIP` only when
there are no blockers; otherwise it signs `NO-SHIP`, leaves the plan open, and
lists every blocker. A `SHIP` decision may state the monthly availability
objective as `pending` only while the honest 30-day window is still open; it
does not publish a 99.9% claim. A missed or overdue window blocks SHIP.

To record an early independent NO-SHIP audit when external evidence does not
exist, omit the dependency flags and mark the affected tasks/gates incomplete
with owned exceptions. Do not fabricate checksums. The missing frozen release,
qualification, production cutover, publication, stabilization, restore, audit,
and retention evidence become explicit blockers.

Verify the signed decision from the immutable store:

~~~bash
.venv/bin/workchord-db-closeout verify \
  --report '<immutable>/postgresql-closure-decision.signed.json' \
  --trusted-public-key '<trust-store>/closure-ed25519-public.pem'
~~~

DBM-CLOSE-001 is complete and the migration contract is closed only when the
independent signed decision says `SHIP`. A signed `NO-SHIP` is valid audit
evidence, but it leaves the plan and failed tasks open. Do not dispose of the
SQLite snapshot from this command; the approved platform retention workflow
does that only after the recorded date and captures secure-disposal evidence.
