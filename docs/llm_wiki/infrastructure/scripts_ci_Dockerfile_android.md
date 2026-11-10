# scripts/ci/Dockerfile.android

**Path:** `scripts/ci/Dockerfile.android`
**Base Image(s):** `eclipse-temurin:17.0.16_8-jdk-jammy@sha256:47d330891da01c4b17fb6af5018d9a7bad33f7a252a91dde890c10d4de5ebd33`

**Configuration view:** source declarations owned by each stage.

Image defaults, variable expansion, and Docker's inheritance/reset rules also affect effective configuration. External base-image defaults remain unknown here.

## Build Stages

### Stage 1

**FROM:** `eclipse-temurin:17.0.16_8-jdk-jammy@sha256:47d330891da01c4b17fb6af5018d9a7bad33f7a252a91dde890c10d4de5ebd33` (source line 1)

**Base relationship:** external or unresolved base; inherited defaults are unknown.

#### Environment Variables

| Variable | Default |
|----------|---------|
| `ANDROID_HOME` | `/opt/android-sdk` |
| `GRADLE_USER_HOME` | `/opt/gradle-cache` |

**Declared WORKDIR:** `/workspace`

#### Entry Point

**CMD:** `["./gradlew", "--no-daemon", "--max-workers=2", "--project-cache-dir", "/tmp/gradle-project-cache", "testDebugUnitTest", "assembleDebug"]`

#### File Copies

| Instruction | Source | Destination | From Stage |
|-------------|--------|-------------|------------|
| `COPY` | `gradlew`, `gradlew.bat`, `gradle.properties`, `settings.gradle.kts`, `build.gradle.kts` | `./` | — |
| `COPY` | `gradle` | `./gradle` | — |
| `COPY` | `app/build.gradle.kts`, `app/proguard-rules.pro` | `./app/` | — |
| `COPY` | `app/src` | `./app/src` | — |

## Notes

The build context is the Android source directory. Explicit COPY instructions exclude SDK-local configuration and signing keys. The wrapper JAR and Gradle distribution have fixed SHA-256 checksums; the archived Android command-line tools are verified against the official repository checksum. Linux amd64 supports the Android build-tool binaries. Material 3 must support the pull-to-refresh API used by the source.
