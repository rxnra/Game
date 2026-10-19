import json
import random
from pathlib import Path

from engine import Question, ROUNDS

QUESTIONS_PATH = "questions.json"
LEADERBOARD_PATH = "leaderboard.json"


class QuestionBank:
    def __init__(self, path: str = QUESTIONS_PATH) -> None:
        with open(path, "r", encoding="utf-8") as file:
            data = json.load(file)

        self._questions: list[Question] = []

        for item in data:
            question = Question(
                text=item["text"],
                options=item["options"],
                correct=item["correct"],
                power_up=item.get("power_up"),
                category=item.get("category", "General Knowledge"),
            )
            self._questions.append(question)

    def categories(self) -> list[str]:
        """Return all categories in the order they first appear."""
        return list(
            dict.fromkeys(question.category for question in self._questions)
        )

    def count(self, category: str | None = None) -> int:
        """Count all questions or questions in one category."""
        if category is None:
            return len(self._questions)

        return sum(
            question.category.casefold() == category.casefold()
            for question in self._questions
        )

    def pick(
        self,
        n: int = ROUNDS,
        category: str | None = None,
    ) -> list[Question]:
        """Select n random questions, optionally from one category."""
        if n < 0:
            raise ValueError("The number of questions cannot be negative.")

        if category is None:
            available_questions = self._questions
        else:
            available_questions = [
                question
                for question in self._questions
                if question.category.casefold() == category.casefold()
            ]

        if n > len(available_questions):
            category_description = (
                f" in category {category!r}"
                if category is not None
                else ""
            )
            raise ValueError(
                f"Requested {n} questions{category_description}, "
                f"but only {len(available_questions)} are available."
            )

        return random.sample(available_questions, k=n)


class ScoreBoard:
    def __init__(self, path: str = LEADERBOARD_PATH) -> None:
        self._path = Path(path)
        self._data: dict[str, dict[str, int]] = {}

        if self._path.exists():
            with open(self._path, encoding="utf-8") as file:
                self._data = json.load(file)

    def is_empty(self) -> bool:
        return not self._data

    def record(self, winner, player1, score1, player2, score2) -> None:
        for name, points in [(player1, score1), (player2, score2)]:
            if name not in self._data:
                self._data[name] = {"wins": 0, "points": 0}

            self._data[name]["points"] += points

        if winner is not None:
            self._data[winner]["wins"] += 1

        self._save()

    def top(self, n: int = 5) -> list[tuple[str, dict[str, int]]]:
        def wins_then_points(item):
            return item[1]["wins"], item[1]["points"]

        return sorted(
            self._data.items(),
            key=wins_then_points,
            reverse=True,
        )[:n]

    def _save(self) -> None:
        with open(self._path, "w", encoding="utf-8") as file:
            json.dump(
                self._data,
                file,
                ensure_ascii=False,
                indent=2,
            )
print("hi")