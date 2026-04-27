from topoaccess_prod.harness.roi_calculator import estimate_roi, scenario_table


def test_estimate_roi_keeps_cost_optional():
    row = estimate_roi(tasks_per_day=100, tokens_per_task=20_000, savings=0.9307)
    assert row["daily_tokens_saved"] == 1_861_400
    assert row["daily_cost_saved"] == 0


def test_scenario_table_includes_public_cases():
    rows = scenario_table(tokens_per_task=10_000)
    assert {row["case"] for row in rows} == {"conservative", "v45_average", "v45_median", "v45_high"}
    assert {row["tasks_per_day"] for row in rows} == {25, 50, 100, 250}
