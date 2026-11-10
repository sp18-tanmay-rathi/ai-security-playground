import pytest

from target.agents import ATTACKS, run_agent


@pytest.mark.parametrize("attack", ATTACKS, ids=lambda a: a["name"])
def test_vulnerable_mock_exhibits_expected_unsafe_behavior(attack):
    result = run_agent("Vulnerable", attack)
    assert result["unsafe"] is True
    assert result["evidence"]


@pytest.mark.parametrize("attack", ATTACKS, ids=lambda a: a["name"])
def test_protected_mock_blocks_unsafe_behavior(attack):
    result = run_agent("Protected", attack)
    assert result["unsafe"] is False
    assert result["severity"] == "None"


def test_unknown_mode_is_rejected():
    with pytest.raises(ValueError):
        run_agent("Production", ATTACKS[0])
