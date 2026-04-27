from topoaccess_prod.harness.prompt_pack import build_prompt_pack


def test_prompt_pack_has_provenance():
    pack = build_prompt_pack("Task")
    assert pack["provenance"]
    assert pack["context_pack_tokens"] < 120000
