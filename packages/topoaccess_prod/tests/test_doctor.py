from topoaccess_prod.install.doctor import run_doctor


def test_doctor_rows():
    assert run_doctor()
