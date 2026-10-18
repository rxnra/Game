# This test assumes your Match class has an
    # answer/submission method that updates the score.
    # Add the actual method call once its name and
    # parameters match your engine.py implementation.
    assert match.players["Alice"] == 0


# -------------------------
# General test
# -------------------------

def test_question_category_is_preserved(bank):
    selected = bank.pick(1, category="English")

    assert selected[0].category == "English"