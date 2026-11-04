import pytest

from course_registration import can_register, late_fee, waitlist_position


def test_can_register_success_and_status_credit_limits():
    assert can_register("regular", 20, 4, True) == "registered"
    assert can_register("probation", 12, 4, True) == "registered"
    assert can_register("honors", 24, 4, True) == "registered"
    assert can_register("regular", 24, 1, True) == "credit limit exceeded"


@pytest.mark.parametrize("status", ["unknown", "", None])
def test_can_register_rejects_unknown_status(status):
    with pytest.raises(ValueError, match="unknown status"):
        can_register(status, 0, 1, True)


@pytest.mark.parametrize("credits", [0, -1])
def test_can_register_rejects_invalid_course_credits(credits):
    with pytest.raises(ValueError, match="invalid course credits"):
        can_register("regular", 0, credits, True)


def test_can_register_reports_missing_prerequisites():
    assert can_register("regular", 0, 3, False) == "prerequisites missing"


def test_waitlist_positions():
    assert waitlist_position(2, 5, 0) == 0
    assert waitlist_position(5, 5, 3) == 4
    assert waitlist_position(7, 5, 10) == -1


@pytest.mark.parametrize("capacity", [0, -1])
def test_waitlist_rejects_invalid_capacity(capacity):
    with pytest.raises(ValueError, match="invalid capacity"):
        waitlist_position(0, capacity, 0)


def test_late_fee_waivers_and_boundaries():
    assert late_fee(0, 5, False) == 0
    assert late_fee(-1, 5, False) == 0
    assert late_fee(5, 5, True) == 0
    assert late_fee(1, 5, False) == 500
    assert late_fee(7, 5, False) == 500
    assert late_fee(8, 5, False) == 600


def test_late_fee_credit_surcharge_and_cap():
    assert late_fee(7, 21, False) == 750
    assert late_fee(30, 21, False) == 2000
