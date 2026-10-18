import json

from storage import QuestionBank, ScoreBoard


SAMPLE = [
    {
        "text": f"Question {i}",
        "options": ["A", "B", "C", "D"],
        "correct": "A",
        "power_up": "double" if i == 1 else None,
        "category": "Test",
    }
    for i in range(1, 9)
]


def make_bank(tmp_path, items=None):
    path = tmp_path / "questions.json"
    with open(path, "w", encoding="utf-8") as file:
        json.dump(SAMPLE if items is None else items, file)

    return QuestionBank(str(path))


def test_bank_loads_questions(tmp_path):
    bank = make_bank(tmp_path)
    assert bank.count() == 8


def test_bank_reads_categories(tmp_path):
    bank = make_bank(tmp_path)
    assert bank.categories() == ["Test"]


def test_bank_preserves_power_ups(tmp_path):
    bank = make_bank(tmp_path)
    questions = bank.pick(8)
    assert any(q.power_up == "double" for q in questions)


def test_picked_questions_are_not_repeated(tmp_path):
    bank = make_bank(tmp_path)
    questions = bank.pick(5)
    assert len({q.text for q in questions}) == 5


def test_cannot_pick_too_many_questions(tmp_path):
    import pytest

    bank = make_bank(tmp_path)
    with pytest.raises(ValueError):
        bank.pick(99)


def test_scoreboard_starts_empty(tmp_path):
    board = ScoreBoard(str(tmp_path / "leaderboard.json"))
    assert board.is_empty()


def test_scoreboard_saves_and_loads_results(tmp_path):
    path = str(tmp_path / "leaderboard.json")

    board = ScoreBoard(path)
    board.record("Sara", "Ali", 10, "Sara", 20)

    loaded_board = ScoreBoard(path)
    results = dict(loaded_board.top())

    assert results["Sara"] == {"wins": 1, "points": 20}
    assert results["Ali"] == {"wins": 0, "points": 10}


def test_scoreboard_adds_points_across_matches(tmp_path):
    board = ScoreBoard(str(tmp_path / "leaderboard.json"))

    board.record("Ali", "Ali", 20, "Reza", 10)
    board.record("Ali", "Ali", 15, "Reza", 30)

    results = dict(board.top())
    assert results["Ali"] == {"wins": 2, "points": 35}


def test_draw_records_points_without_a_win(tmp_path):
    board = ScoreBoard(str(tmp_path / "leaderboard.json"))
    board.record(None, "Ali", 12, "Reza", 12)

    results = dict(board.top())
    assert results["Ali"] == {"wins": 0, "points": 12}
    assert results["Reza"] == {"wins": 0, "points": 12}