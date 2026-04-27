from topoaccess_prod.release.dist_smoke import dist_smoke


def test_dist_smoke_function_exists():
    assert callable(dist_smoke)

