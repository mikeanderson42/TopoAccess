from pathlib import Path

from topoaccess_prod.release.ci_templates import GITHUB_WORKFLOW, LOCAL_CI


def test_ci_templates_include_required_steps():
    assert "pytest packages/topoaccess_prod/tests" in LOCAL_CI
    assert "topoaccess_artifact_audit.py" in LOCAL_CI
    assert "TopoAccess Product CI" in GITHUB_WORKFLOW

