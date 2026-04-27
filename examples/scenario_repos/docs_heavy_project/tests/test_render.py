from docs_app.render import render_title


def test_render_title():
    assert render_title(" Guide ") == "# Guide"
