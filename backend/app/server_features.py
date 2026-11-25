"""Server features a client can detect before it holds a credential.

A client such as a read-only dashboard reads this list from ``GET /api/auth/me``
to choose what to use, instead of comparing versions or commits. A name is
stable once published; a server without a feature does not list it.
"""

SERVER_FEATURES = (
    # Pairing a read-only observer session, on managed and trusted-local servers,
    # and renewal that keeps the access level and stops at an absolute cap.
    "observer-sessions-v1",
    # GET /api/agent/assignments without an agent key.
    "person-assignment-reads-v1",
    # GET /api/agent/team-setup/topology with runtime references.
    "team-topology-read-v1",
    # External links with provider "agdash", which may use a loopback URL.
    "agdash-external-links-v1",
    # metadata.harness declared at begin, searchable on runs.
    "harness-session-metadata-v1",
    # POST and GET /api/agent/observations, advisory only.
    "runtime-observations-v1",
    # GET /api/agent/runs without an agent key.
    "person-run-reads-v1",
    # PATCH /api/tasks/{task_id}/delivery-dependencies/{edge_id} changes or clears
    # a prerequisite's target branch.
    "delivery-prerequisite-retarget-v1",
)
