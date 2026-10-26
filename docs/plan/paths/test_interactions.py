"""interactions.non_additive flags a joint row only when no single-option run predicts it.

Run: python -m pytest -q -p no:cacheprovider docs/plan/paths/test_interactions.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import interactions as m  # noqa: E402

BASE = {"x": 1, "y": 1}
A = {"x": 2, "y": 1}
B = {"x": 1, "y": 3}


def test_independent_options_combine():
    assert m.non_additive(BASE, [A, B], {"x": 2, "y": 3}) == []


def test_a_value_neither_option_gives_is_flagged():
    assert m.non_additive(BASE, [A, B], {"x": 5, "y": 3}) == ["x"]


def test_a_joint_that_drops_both_changes_is_flagged():
    assert m.non_additive(BASE, [A, B], {"x": 1, "y": 1}) == ["x", "y"]


def test_both_options_move_a_row_and_the_joint_takes_neither():
    assert m.non_additive(BASE, [{"x": 2}, {"x": 3}], {"x": 2.5}) == ["x"]


def test_a_row_only_the_joint_has_is_flagged():
    assert m.non_additive(BASE, [A, B], {"x": 2, "y": 3, "z": 0}) == ["z"]
