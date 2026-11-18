"""Parse GitHub URLs that trace delivery work: pull requests, issues, branches, commits and tags."""
from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Any, Optional
from urllib.parse import urlparse

SUPPORTED_GITHUB_LINKS_MESSAGE = (
    "Only GitHub pull request, issue, branch, commit, and tag URLs are supported"
)
# A full SHA-1 or SHA-256 object name. A short SHA can become ambiguous, and two
# spellings of one commit would defeat duplicate detection.
_FULL_COMMIT_SHA = re.compile(r"^(?:[0-9a-f]{40}|[0-9a-f]{64})$")


class GitHubLinkError(ValueError):
    """Raised when a URL is not a supported GitHub link."""


@dataclass(frozen=True)
class ParsedGitHubLink:
    """Normalized GitHub link details ready for persistence."""

    github_type: str
    owner: str
    repo: str
    repo_full_name: str
    number: Optional[int]
    branch: Optional[str]
    external_key: str
    url: str
    title: str
    sha: Optional[str] = None
    tag: Optional[str] = None

    @property
    def metadata_json(self) -> dict[str, Any]:
        """Return the public metadata stored with the external link."""
        metadata: dict[str, Any] = {
            "github_type": self.github_type,
            "owner": self.owner,
            "repo": self.repo,
            "repo_full_name": self.repo_full_name,
        }
        if self.number is not None:
            metadata["number"] = self.number
        if self.branch is not None:
            metadata["branch"] = self.branch
        if self.sha is not None:
            metadata["sha"] = self.sha
        if self.tag is not None:
            metadata["tag"] = self.tag
        return metadata


def _commit(owner: str, repo: str, raw_sha: str) -> ParsedGitHubLink:
    sha = raw_sha.lower()
    if not _FULL_COMMIT_SHA.match(sha):
        raise GitHubLinkError("GitHub commit URLs must use the full commit SHA")
    repo_full_name = f"{owner}/{repo}"
    return ParsedGitHubLink(
        github_type="commit",
        owner=owner,
        repo=repo,
        repo_full_name=repo_full_name,
        number=None,
        branch=None,
        sha=sha,
        external_key=f"{repo_full_name}@{sha}",
        url=f"https://github.com/{repo_full_name}/commit/{sha}",
        title=f"{repo_full_name} commit {sha[:12]}",
    )


def parse_github_url(raw_url: str) -> ParsedGitHubLink:
    """Parse a GitHub pull request, issue, branch, commit, or release tag URL."""
    url = (raw_url or "").strip()
    if not url:
        raise GitHubLinkError("GitHub URL is required")

    parsed = urlparse(url if "://" in url else f"https://{url}")
    hostname = (parsed.hostname or "").lower()
    if parsed.scheme not in {"http", "https"} or hostname not in {
        "github.com",
        "www.github.com",
    }:
        raise GitHubLinkError(SUPPORTED_GITHUB_LINKS_MESSAGE)

    parts = [part for part in parsed.path.strip("/").split("/") if part]
    if len(parts) < 4:
        raise GitHubLinkError(SUPPORTED_GITHUB_LINKS_MESSAGE)

    owner, repo, link_type = parts[0], parts[1], parts[2]
    repo_full_name = f"{owner}/{repo}"

    if link_type == "pull" and parts[3].isdigit():
        if len(parts) >= 6 and parts[4] == "commits":
            return _commit(owner, repo, parts[5])
        number = int(parts[3])
        return ParsedGitHubLink(
            github_type="pull_request",
            owner=owner,
            repo=repo,
            repo_full_name=repo_full_name,
            number=number,
            branch=None,
            external_key=f"{repo_full_name}#{number}",
            url=f"https://github.com/{repo_full_name}/pull/{number}",
            title=f"{repo_full_name} PR #{number}",
        )

    if link_type == "issues" and parts[3].isdigit():
        number = int(parts[3])
        return ParsedGitHubLink(
            github_type="issue",
            owner=owner,
            repo=repo,
            repo_full_name=repo_full_name,
            number=number,
            branch=None,
            external_key=f"{repo_full_name}#{number}",
            url=f"https://github.com/{repo_full_name}/issues/{number}",
            title=f"{repo_full_name} issue #{number}",
        )

    if link_type == "commit" and len(parts) == 4:
        return _commit(owner, repo, parts[3])

    if link_type == "releases" and len(parts) >= 5 and parts[3] == "tag":
        tag = "/".join(parts[4:]).strip("/")
        if tag:
            return ParsedGitHubLink(
                github_type="tag",
                owner=owner,
                repo=repo,
                repo_full_name=repo_full_name,
                number=None,
                branch=None,
                tag=tag,
                external_key=f"{repo_full_name}@refs/tags/{tag}",
                url=f"https://github.com/{repo_full_name}/releases/tag/{tag}",
                title=f"{repo_full_name} tag {tag}",
            )

    if link_type == "tree":
        branch = "/".join(parts[3:]).strip("/")
        if branch:
            return ParsedGitHubLink(
                github_type="branch",
                owner=owner,
                repo=repo,
                repo_full_name=repo_full_name,
                number=None,
                branch=branch,
                external_key=f"{repo_full_name}@{branch}",
                url=f"https://github.com/{repo_full_name}/tree/{branch}",
                title=f"{repo_full_name} branch {branch}",
            )

    raise GitHubLinkError(SUPPORTED_GITHUB_LINKS_MESSAGE)


def require_github_link(raw_url: str, github_type: str) -> str:
    """Return the normalized URL when it is a GitHub link of the given type."""
    parsed = parse_github_url(raw_url)
    if parsed.github_type != github_type:
        raise GitHubLinkError(
            f"Expected a GitHub {github_type.replace('_', ' ')} URL, got a {parsed.github_type.replace('_', ' ')} URL"
        )
    return parsed.url
