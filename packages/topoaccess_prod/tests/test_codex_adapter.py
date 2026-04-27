from topoaccess_prod.integrations.codex_adapter import codex_brief


def test_codex_brief_has_provenance_and_tests():
    brief = codex_brief("Improve command lookup")
    assert brief["provenance"]
    assert brief["tests_to_run"]
