from engine.report import build_markdown_report
from engine.runner import run_suite


def test_compare_runs_five_cases_against_both_targets():
    results = run_suite("Compare both")
    assert len(results) == 10
    assert sum(r["outcome"] == "FAIL" for r in results if r["target"] == "Vulnerable") == 5
    assert sum(r["outcome"] == "PASS" for r in results if r["target"] == "Protected") == 5


def test_single_target_selection():
    assert len(run_suite("Vulnerable demo agent")) == 5
    assert len(run_suite("Protected demo agent")) == 5


def test_unknown_target_is_rejected():
    try:
        run_suite("Something else")
    except ValueError:
        pass
    else:
        raise AssertionError("Expected ValueError")


def test_report_contains_scope_warning_and_results():
    report = build_markdown_report(run_suite("Compare both"), "demo time")
    assert "# AI Security Playground" in report
    assert "not a security certification" in report
    assert "Unauthorized tool use" in report
