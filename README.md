# WorkChord

WorkChord is a self-hosted project workspace for teams of people and external agents. Plan an iteration around the hours your team has, see which tasks depend on each other, and review the evidence before accepting the work.

[Download the demo (1:45)](docs/media/workchord-demo.mp4) · [Try the sample project](#get-started) · [Connect an agent](docs/agent-team-setup.md) · [Deploy a shared workspace](docs/runbooks/self-hosted-server-acceptance.md)

https://github.com/user-attachments/assets/e1d3cfab-8568-4333-8b41-4c823e9b12eb

*Eight tasks make up the sample welcome guide. Follow the two lines into “Review the draft” to see which pieces have to be ready together. The person and robot icons show who owns each task.* [English captions](docs/media/workchord-demo.en.vtt)

## Get started

To try the sample on your own machine, use Git and Docker Compose v2. Run these commands in a Bash-compatible shell. The demo gets its own PostgreSQL volume and uses trusted-local access on the loopback address.

```bash
git clone https://github.com/Denissvgn/WorkChord.git
cd WorkChord
WORKCHORD_AUTH_MODE=trusted_local docker compose --env-file .env.example -p workchord-demo up --build --detach
```

1. Open [localhost](http://localhost). In **Overview → Get started → Say who you are**, enter a name and choose **Add me**.
2. Choose **Load a sample project**. **Plan** opens on *Sample first iteration*. Expand **Capacity** to see how the person and the sample agent share the work.
3. Open **Gantt** and select **Sample: Agree on the audience**. The brief asks for three questions a new teammate needs answered and tells the reviewer how to check the result.
4. Choose **Start work**, then reopen the task in **My Work → Doing**. Record your answer in **Work & review** and submit it. After a reviewer accepts it, **Analytics** counts the task under **Accepted deliverables**.

To stop the demo and keep its data, run `docker compose --env-file .env.example -p workchord-demo stop`.

For a shared deployment, WorkChord defaults to managed sign-in. Configure an OIDC provider and an operator key, then establish the first workspace owner. [Identity and recovery](docs/identity-and-recovery.md) · [Server setup](docs/runbooks/self-hosted-server-acceptance.md)

## Working in WorkChord

| When you need to… | Where to go |
| --- | --- |
| Turn a request into work | **Triage** sends requests to a project backlog. In **Tasks**, give each task an assignee, an estimate in hours, and acceptance criteria. [Teamwork guide](docs/human-teamwork.md) |
| Decide what fits | **Plan** accounts for work calendars, absences, dependencies, and capacity shared across projects. Preview the schedule before applying dates. [Iteration planning](docs/human-teamwork.md#plan-iterations-and-capacity) |
| Hand work to an agent | **Team → Connect** sets up an external agent. Its own runtime claims assignments and returns evidence over authenticated REST or the Model Context Protocol (MCP). The sample includes an agent profile so you can explore planning before connecting a runtime. [Runtime guide](docs/external-agent-runtime.md) |
| Decide whether work is done | **My Work** shows what to do and what needs review. Open **Work & review** to record evidence for each criterion. A reviewer can accept the result or request changes. [Task and review semantics](docs/task-domain.md) |
| Measure delivery | **Analytics** counts accepted deliverables and shows lead time, cycle time, and review delay. With optional time recording, people keep private entries and project managers can see totals. [Delivery metrics](docs/delivery-analytics.md) · [Recorded time](docs/time-entries.md) |

The web app supports English and Russian. The Android companion gives people access to their tasks from a phone. [Android companion](android-companion/)

## Documentation

- **Run from source** with Python, Node.js, and a local SQLite database. [Local development](docs/local-development.md)
- **Operate PostgreSQL** and keep a recoverable copy of your workspace. [Deployment](docs/runbooks/postgresql-deployment.md) · [Operations](docs/runbooks/postgresql-operations.md) · [Backup and restore](docs/runbooks/postgresql-backup-restore.md) · [Troubleshooting](docs/runbooks/postgresql-troubleshooting.md)
- **Configure or upgrade a workspace.** [Environment settings](.env.example) · [Release 1.9.0 notes](docs/releases/1.9.0.md) · [Interface upgrade notes](docs/releases/interface-1.1.md)

## License

WorkChord is available under the MIT license. [License](LICENSE) · [Third-party notices](THIRD_PARTY_NOTICES.md) · [Sponsor WorkChord](https://github.com/sponsors/Denissvgn)
