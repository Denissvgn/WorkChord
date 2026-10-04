# build_agent_skills

**Entry point:** `main` (`process`)
**Source:** [build_agent_skills](../modules/build_agent_skills.md)
**Modules touched:** [build_agent_skills](../modules/build_agent_skills.md)

## Call sequence

<!-- Auto-generated from static call edges. Dashed arrows are external or unresolved calls. Reviewed runtime conditions and side effects belong in Behavior. -->
```mermaid
sequenceDiagram
    participant p0 as main
    participant p1 as _parser().parse_args
    participant p2 as _parser
    participant p3 as argparse.ArgumentParser
    participant p4 as parser.add_argument
    participant p5 as parser.add_subparsers
    participant p6 as subparsers.add_parser
    participant p7 as build_parser.add_argument
    participant p8 as archive_parser.add_argument
    participant p9 as sorted (scripts/build_agent_skills.py:_parser)
    participant p10 as codex_parser.add_argument
    participant p11 as install_parser.add_argument
    participant p12 as installed_parser.add_argument
    p0-->>p1: _parser().parse_args
    p0->>p2: _parser
    p2-->>p3: argparse.ArgumentParser
    p2-->>p4: parser.add_argument
    p2-->>p5: parser.add_subparsers
    p2-->>p6: subparsers.add_parser
    p2-->>p6: subparsers.add_parser
    p2-->>p6: subparsers.add_parser
    p2-->>p6: subparsers.add_parser
    p2-->>p6: subparsers.add_parser
    p2-->>p6: subparsers.add_parser
    p2-->>p7: build_parser.add_argument
    p2-->>p6: subparsers.add_parser
    p2-->>p8: archive_parser.add_argument
    p2-->>p8: archive_parser.add_argument
    p2-->>p9: sorted (scripts/build_agent_skills.py:_parser)
    p2-->>p6: subparsers.add_parser
    p2-->>p10: codex_parser.add_argument
    p2-->>p6: subparsers.add_parser
    p2-->>p11: install_parser.add_argument
    p2-->>p11: install_parser.add_argument
    p2-->>p11: install_parser.add_argument
    p2-->>p9: sorted (scripts/build_agent_skills.py:_parser)
    p2-->>p11: install_parser.add_argument
    p2-->>p11: install_parser.add_argument
    p2-->>p6: subparsers.add_parser
    p2-->>p12: installed_parser.add_argument
    p2-->>p12: installed_parser.add_argument
    p2-->>p12: installed_parser.add_argument
    p2-->>p9: sorted (scripts/build_agent_skills.py:_parser)
```

> Call sequence diagram shows 30 of 1164 interactions; 1134 omitted to keep the visualization within the 30-interaction and generated-diagram limits.

> Trace truncated at the depth limit; deeper calls are omitted.

## Data flow

<!-- Auto-generated static analysis. Treat values and boundaries as best-effort hints, not runtime proof. -->
```mermaid
flowchart LR
    s1["1. main"]
    s2["2. _parser().parse_args"]
    s3["3. _parser"]
    s4["4. argparse.ArgumentParser"]
    s5["5. parser.add_argument"]
    s6["6. parser.add_subparsers"]
    s7["7. subparsers.add_parser"]
    s8["8. subparsers.add_parser"]
    s9["9. subparsers.add_parser"]
    s10["10. subparsers.add_parser"]
    s11["11. subparsers.add_parser"]
    s12["12. subparsers.add_parser"]
    s1 -. "_parser().parse_args(argv)" .-> s2
    s1 -->|"_parser(data not statically known)"| s3
    s3 -. "argparse.ArgumentParser(description=__doc__)" .-> s4
    s3 -. "parser.add_argument('--skills-dir', type=Path, default=DEFAULT_SKILLS_DIR, help='Canonical agent-skills directory (default: repository agent-skills)')" .-> s5
    s3 -. "parser.add_subparsers(dest='command', required=True)" .-> s6
    s3 -. "subparsers.add_parser('sync-generated', help='Synchronize shared contract blocks and role openai.yaml adapters')" .-> s7
    s3 -. "subparsers.add_parser('contract-json', help='Print the canonical machine-readable assigned-work v1 contract')" .-> s8
    s3 -. "subparsers.add_parser('generate', help='Regenerate catalog.json from role folders')" .-> s9
    s3 -. "subparsers.add_parser('freeze-release', help='Append current exact role versions to the immutable release baseline')" .-> s10
    s3 -. "subparsers.add_parser('validate', help='Validate role folders and catalog.json')" .-> s11
    s3 -. "subparsers.add_parser('build', help='Build reproducible role archives')" .-> s12
    b0["output print"]
    s1 -. "output print" .-> b0
    b1["output print"]
    s1 -. "output print" .-> b1
    b2["output print"]
    s1 -. "output print" .-> b2
    b3["output print"]
    s1 -. "output print" .-> b3
    b4["output print"]
    s1 -. "output print" .-> b4
    b5["output print"]
    s1 -. "output print" .-> b5
    b6["output print"]
    s1 -. "output print" .-> b6
    b7["output print"]
    s1 -. "output print" .-> b7
    click s1 "../modules/build_agent_skills.md"
    click s3 "../modules/build_agent_skills.md"
    classDef boundary stroke:#b45309,stroke-dasharray: 4 2
    class b0 boundary
    class b1 boundary
    class b2 boundary
    class b3 boundary
    class b4 boundary
    class b5 boundary
    class b6 boundary
    class b7 boundary
```

### Step data

| Step | Inputs | Reads | Writes | Returns |
|---|---|---|---|---|
| `main` | `argv: list[str] \| None` | `REPOSITORY_ROOT`, `ASSIGNED_WORK_V1_CONTRACT`, `SkillPackError`, `sys` | - | `2`, `0` |
| `_parser().parse_args` | - | - | - | - |
| `_parser` | - | `Path`, `DEFAULT_SKILLS_DIR`, `Path`, `Path`, `ROLE_METADATA`, `Path`, `Path`, `Path` | - | `parser` |
| `argparse.ArgumentParser` | - | - | - | - |
| `parser.add_argument` | - | - | - | - |
| `parser.add_subparsers` | - | - | - | - |
| `subparsers.add_parser` | - | - | - | - |
| `subparsers.add_parser` | - | - | - | - |
| `subparsers.add_parser` | - | - | - | - |
| `subparsers.add_parser` | - | - | - | - |
| `subparsers.add_parser` | - | - | - | - |
| `subparsers.add_parser` | - | - | - | - |

### Call data

| From | To | Line | Call |
|---|---|---:|---|
| main | _parser().parse_args | 3079 | `_parser().parse_args(argv)` |
| main | _parser | 3079 | `_parser(data not statically known)` |
| _parser | argparse.ArgumentParser | 3020 | `argparse.ArgumentParser(description=__doc__)` |
| _parser | parser.add_argument | 3021 | `parser.add_argument('--skills-dir', type=Path, default=DEFAULT_SKILLS_DIR, help='Canonical agent-skills directory (default: repository agent-skills)')` |
| _parser | parser.add_subparsers | 3027 | `parser.add_subparsers(dest='command', required=True)` |
| _parser | subparsers.add_parser | 3028 | `subparsers.add_parser('sync-generated', help='Synchronize shared contract blocks and role openai.yaml adapters')` |
| _parser | subparsers.add_parser | 3032 | `subparsers.add_parser('contract-json', help='Print the canonical machine-readable assigned-work v1 contract')` |
| _parser | subparsers.add_parser | 3036 | `subparsers.add_parser('generate', help='Regenerate catalog.json from role folders')` |
| _parser | subparsers.add_parser | 3037 | `subparsers.add_parser('freeze-release', help='Append current exact role versions to the immutable release baseline')` |
| _parser | subparsers.add_parser | 3041 | `subparsers.add_parser('validate', help='Validate role folders and catalog.json')` |
| _parser | subparsers.add_parser | 3042 | `subparsers.add_parser('build', help='Build reproducible role archives')` |

### Boundary effects

| Kind | Target | Step | Line |
|---|---|---|---:|
| output | `print` | `main` | 3088 |
| output | `print` | `main` | 3093 |
| output | `print` | `main` | 3096 |
| output | `print` | `main` | 3099 |
| output | `print` | `main` | 3102 |
| output | `print` | `main` | 3108 |
| output | `print` | `main` | 3111 |
| output | `print` | `main` | 3120 |

### Static analysis gaps

| Kind | Step | Target | Line |
|---|---|---|---:|
| unresolved_call | `main` | `_parser().parse_args` | 3079 |
| external_call | `_parser` | `argparse.ArgumentParser` | 3020 |
| unresolved_call | `_parser` | `parser.add_argument` | 3021 |
| unresolved_call | `_parser` | `parser.add_subparsers` | 3027 |
| unresolved_call | `_parser` | `subparsers.add_parser` | 3028 |
| unresolved_call | `_parser` | `subparsers.add_parser` | 3032 |
| unresolved_call | `_parser` | `subparsers.add_parser` | 3036 |
| unresolved_call | `_parser` | `subparsers.add_parser` | 3037 |
| unresolved_call | `_parser` | `subparsers.add_parser` | 3041 |
| unresolved_call | `_parser` | `subparsers.add_parser` | 3042 |
| step_limit | `main` | `first 12 steps` | 0 |
| truncated_flow | `main` | `depth limit` | 0 |

## Behavior

This flow starts at `main` and is classified as `process`. The generated call and data-flow sections are bounded static projections; runtime conditions and side effects require source-level confirmation.
