ROUNDS = 5          # Number of rounds per match
TIME_LIMIT = 30     # Time limit per answer, in seconds
POINTS = 10         # Points for a correct answer
SPEED_BONUS = 3     # Bonus for the fastest correct answer


class Question:
    def __init__(
        self,
        text,
        options,
        correct,
        power_up=None,
        category="",
    ):
        if len(options) != 4:
            raise ValueError("Every question must have exactly 4 options.")

        correct = str(correct).strip().upper()
        if correct not in ("A", "B", "C", "D"):
            raise ValueError(
                f"The correct answer must be A, B, C, or D, not {correct!r}"
            )

        self.text = text
        self.options = options
        self.correct = correct
        self.power_up = power_up
        self.category = category

    def is_correct(self, choice):
        return str(choice).strip().upper() == self.correct

    def correct_text(self):
        return self.options["ABCD".index(self.correct)]


class RoundResult:
    def __init__(self, status, points):
        self.status = status
        self.points = points


class Match:
    def __init__(self, player1, player2, questions):
        if player1 == player2:
            raise ValueError("Unique Name per Player!")

        if len(questions) < ROUNDS:
            raise ValueError(
                f"Each match requires at least {ROUNDS} questions."
            )

        self.players = [player1, player2]
        self.questions = questions
        self.scores = {player1: 0, player2: 0}
        self.round = 0
        self.answers = {}

    def start_round(self):
        if self.round >= len(self.questions):
            return None

        self.round += 1
        self.answers = {}
        return self.questions[self.round - 1]

    def score_of(self, player):
        return self.scores[player]

    def submit(self, player, choice, elapsed):
        if player not in self.players:
            raise ValueError(f"Unknown player: {player}")

        self.answers[player] = (choice, elapsed)

    def resolve_round(self):
        if self.round == 0:
            return {}

        question = self.questions[self.round - 1]
        results = {}
        correct_players = []

        # 1. Check whether each answer is correct or too late.
        for player in self.players:
            if player not in self.answers:
                continue

            choice, elapsed = self.answers[player]

            if elapsed > TIME_LIMIT:
                results[player] = RoundResult("too_late", 0)
            elif question.is_correct(choice):
                results[player] = RoundResult("correct", POINTS)
                correct_players.append(player)
            else:
                results[player] = RoundResult("wrong", 0)

        # 2. Give a speed bonus to the fastest correct answer.
        if correct_players:
            fastest = min(
                correct_players,
                key=lambda player: self.answers[player][1],
            )
            results[fastest].points += SPEED_BONUS

        # 3. Double points for correct answers on a double-power-up question.
        if question.power_up == "double":
            for player in correct_players:
                results[player].points *= 2

        # 4. Update scores.
        for player, result in results.items():
            self.scores[player] += result.points

        return results

    def is_over(self):
        return self.round >= len(self.questions)

    def winner(self):
        player1, player2 = self.players

        if self.scores[player1] == self.scores[player2]:
            return None

        if self.scores[player1] > self.scores[player2]:
            return player1

        return player2