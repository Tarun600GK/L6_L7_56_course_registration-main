import pytest

from course_registration import can_register, late_fee, waitlist_position


@pytest.mark.parametrize(
    ("status", "current", "credits", "prerequisites", "expected"),
    [
        ("regular", 20, 4, True, "registered"),
        ("probation", 12, 4, True, "registered"),
        ("honors", 24, 4, True, "registered"),
        ("regular", 24, 1, True, "credit limit exceeded"),
        ("regular", 0, 3, False, "prerequisites missing"),
    ],
)
def test_can_register_decision_outcomes(
    status, current, credits, prerequisites, expected
):
    assert can_register(status, current, credits, prerequisites) == expected


@pytest.mark.parametrize("status", ["unknown", "", None])
def test_can_register_unknown_status_branch(status):
    with pytest.raises(ValueError, match="unknown status"):
        can_register(status, 0, 1, True)


@pytest.mark.parametrize("credits", [0, -1])
def test_can_register_invalid_credits_branch(credits):
    with pytest.raises(ValueError, match="invalid course credits"):
        can_register("regular", 0, credits, True)


@pytest.mark.parametrize(
    ("enrolled", "capacity", "waitlist_length", "expected"),
    [(2, 5, 0, 0), (5, 5, 3, 4), (7, 5, 10, -1)],
)
def test_waitlist_decision_outcomes(enrolled, capacity, waitlist_length, expected):
    assert waitlist_position(enrolled, capacity, waitlist_length) == expected


@pytest.mark.parametrize("capacity", [0, -1])
def test_waitlist_invalid_capacity_branch(capacity):
    with pytest.raises(ValueError, match="invalid capacity"):
        waitlist_position(0, capacity, 0)


@pytest.mark.parametrize(
    ("days_late", "credits", "waiver", "expected"),
    [
        (0, 5, False, 0),
        (-1, 5, False, 0),
        (5, 5, True, 0),
        (1, 5, False, 500),
        (7, 5, False, 500),
        (8, 5, False, 600),
        (7, 21, False, 750),
        (30, 21, False, 2000),
        (30, 20, False, 2000),
    ],
)
def test_late_fee_decision_outcomes(days_late, credits, waiver, expected):
    assert late_fee(days_late, credits, waiver) == expected
