from topoaccess_prod.install.doctor_fixes import suggested_fixes


def test_doctor_fixes_suggest_missing_cache():
    fixes = suggested_fixes("missing-cache", "missing-search")
    assert any("Cache missing" in fix for fix in fixes)

