"""A concise entrypoint still binds release evidence to authoritative operator policy."""

import shutil

import pytest

from app.database_migration.closeout import REPOSITORY_DOCUMENTS, CloseoutEvidenceError, _repository_document_set


def test_linked_operator_boundary_cannot_be_removed_from_release_docs(tmp_path):
    from pathlib import Path
    root = Path(__file__).resolve().parents[3]
    for relative in [*REPOSITORY_DOCUMENTS.values(), Path("backend/pyproject.toml"), Path("backend/app/main.py")]:
        target = tmp_path / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(root / relative, target)
    _repository_document_set(tmp_path, expected_application_version="1.7.0")
    operator = tmp_path / "docs/runbooks/postgresql-operations.md"
    operator.write_text(operator.read_text().replace("It cannot certify 1,250 authenticated people.", "No capacity statement."))
    with pytest.raises(CloseoutEvidenceError, match="cannot certify"):
        _repository_document_set(tmp_path, expected_application_version="1.7.0")
