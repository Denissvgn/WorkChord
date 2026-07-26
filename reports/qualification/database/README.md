# Database qualification workspace

Generated PostgreSQL scale, resilience, restore, and signed qualification
artifacts are assembled here during an authorized rehearsal. This directory is
not evidence by itself and currently contains no completed qualification.

Follow `docs/runbooks/postgresql-qualification.md`. Transfer each attempt to
the approved immutable evidence store, retain it for the contract period, and
never place credentials, browser/session tokens, agent API keys, database
passwords, or private signing keys in this tree.

DBM-REHEARSE-001 and DBM-CUT-002 records follow
`docs/runbooks/postgresql-rehearsal-cutover-evidence.md`. A local sealed or
signed JSON file is still not proof that a rehearsal or production cutover
occurred; acceptance requires the trusted signer keys, source/change-system
evidence, and the complete dependency chain described there.

DBM-DOC-002 publications and DBM-CLOSE-001 SHIP/NO-SHIP decisions follow
`docs/runbooks/postgresql-postcutover-release-and-closeout.md`. Keep rendered
release notes, post-cutover observations, backup/restore evidence, availability
denominators, and signed decisions in the approved immutable store. Missing
production evidence remains NO-SHIP; this workspace does not imply otherwise.
