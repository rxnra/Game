import pytest

from engine import Match, Question, ROUNDS, POINTS, SPEED_BONUS, TIME_LIMIT


def make_questions():
    return [
        Question("2 + 2?", ["4", "5", "6", "7"], "A")
        for _ in range(ROUNDS)
    ]


def make_match():
    return Match("Ali", "Reza", make_questions())


def test_correct_answer_gets_points():
    match = make_match()
    match.start_round()
    match.submit("Ali", "A", 5.0)
    match.submit("Reza", "B", 8.0)
    results = match.resolve_round()

    assert results["Ali"].status == "correct"
    assert match.score_of("Ali") == POINTS + SPEED_BONUS
    assert match.score_of("Reza") == 0


def test_wrong_answer_gets_no_points():
    match = make_match()
    match.start_round()
    match.submit("Ali", "B", 2.0)
    match.submit("Reza", "C", 3.0)
    match.resolve_round()

    assert match.score_of("Ali") == 0
    assert match.score_of("Reza") == 0


def test_late_answer_gets_no_points():
    match = make_match()
    match.start_round()
    match.submit("Ali", "A", TIME_LIMIT + 1)
    match.submit("Reza", "B", 5.0)
    results = match.resolve_round()

    assert results["Ali"].status == "too_late"
    assert match.score_of("Ali") == 0


def test_answer_is_case_insensitive():
    match = make_match()
    match.start_round()
    match.submit("Ali", " a ", 5.0)
    match.submit("Reza", "B", 8.0)
    match.resolve_round()

    assert match.score_of("Ali") == POINTS + SPEED_BONUS


def test_match_winner():
    match = make_match()

    for _ in range(ROUNDS):
        match.start_round()
        match.submit("Ali", "A", 2.0)
        match.submit("Reza", "B", 2.0)
        match.resolve_round()

    assert match.is_over()
    assert match.winner() == "Ali"


def test_draw_has_no_winner():
    match = make_match()

    for _ in range(ROUNDS):
        match.start_round()
        match.submit("Ali", "B", 2.0)
        match.submit("Reza", "C", 2.0)
        match.resolve_round()

    assert match.winner() is None


def test_duplicate_player_names_are_rejected():
    with pytest.raises(ValueError):
        Match("Ali", "Ali", make_questions())


def test_insufficient_questions_are_rejected():
    with pytest.raises(ValueError):
        Match("Ali", "Reza", make_questions()[:2])


def test_question_requires_four_options():
    with pytest.raises(ValueError):
        Question("2 + 2?", ["4", "5"], "A")


def test_invalid_correct_answer_is_rejected():
    with pytest.raises(ValueError):
        Question("2 + 2?", ["4", "5", "6", "7"], "E")