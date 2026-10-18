import time

from rich.console import Console

from engine import Match, ROUNDS
from storage import QuestionBank, ScoreBoard
from app_log import AppLog

AppLog.setup()
console = Console()


def show_menu():
    console.print("\nQuiz Battle", style="bold cyan")
    console.print("۱) بازی جدید", style="bold green")
    console.print("۲) خروج", style="bold red")


def show_leaderboard(board):
    console.print("\nرده‌بندی کل", style="bold cyan")

    if board.is_empty():
        console.print("  هنوز هیچ مسابقه‌ای ثبت نشده.")
        return

    for rank, (name, stat) in enumerate(board.top(5), start=1):
        console.print(
            f"  {rank}) {name} — "
            f"{stat['wins']} برد، {stat['points']} امتیاز"
        )


def choose_category(bank):
    categories = bank.categories()

    if not categories:
        console.print("هیچ دسته‌بندی‌ای وجود ندارد.", style="red")
        return None

    console.print("\nانتخاب موضوع", style="bold cyan")

    for number, category in enumerate(categories, start=1):
        count = bank.count(category)
        console.print(
            f"{number}) {category} ({count} سؤال)",
            style="bold",
        )

    while True:
        choice = input("شماره یا نام موضوع را وارد کن: ").strip()

        selected_category = None

        if choice.isdigit():
            index = int(choice) - 1

            if 0 <= index < len(categories):
                selected_category = categories[index]
        else:
            for category in categories:
                if category.casefold() == choice.casefold():
                    selected_category = category
                    break

        if selected_category is None:
            console.print(
                "لطفاً یک شماره یا نام موضوع معتبر وارد کن.",
                style="yellow",
            )
            continue

        if bank.count(selected_category) < ROUNDS:
            console.print(
                f"برای این موضوع حداقل {ROUNDS} سؤال لازم است.",
                style="yellow",
            )
            continue

        return selected_category


def prompt_choice(player_name, question):
    console.print(f"\n{player_name}", style="bold cyan")
    console.print(question.text, style="bold")

    for letter, option in zip("ABCD", question.options):
        console.print(f"  {letter}) {option}", style="bold")

    while True:
        start = time.perf_counter()
        choice = input("جواب تو (A-D): ").strip().upper()
        elapsed = time.perf_counter() - start

        if choice in ("A", "B", "C", "D"):
            return choice, elapsed

        console.print(
            "لطفاً فقط یکی از گزینه‌های A تا D را وارد کن.",
            style="yellow",
        )


def play_match(
    questions,
    player1_name="بازیکن 1",
    player2_name="بازیکن 2",
):
    match = Match(player1_name, player2_name, questions)

    while not match.is_over():
        question = match.start_round()

        console.print(
            f"\nراند {match.round} از {ROUNDS}",
            style="bold yellow",
        )

        for player in match.players:
            choice, elapsed = prompt_choice(player, question)
            match.submit(player, choice, elapsed)

        results = match.resolve_round()

        for player, result in results.items():
            if result.status == "too_late":
                console.print(
                    f"  {player}: زمان تمام شد",
                    style="red",
                )
            elif result.status == "correct":
                console.print(
                    f"  {player}: درست (+{result.points})",
                    style="green",
                )
            else:
                console.print(
                    f"  {player}: اشتباه — "
                    f"جواب درست: {question.correct_text()}",
                    style="red",
                )

        console.print("\nامتیاز فعلی:", style="bold")

        for player in match.players:
            console.print(
                f"  {player}: {match.score_of(player)}",
                style="green",
            )
def main():
    bank = QuestionBank()
    board = ScoreBoard()

    while True:
        show_menu()
        choice = input("\nشماره گزینه را وارد کن: ").strip()

        if choice == "1":
            category = choose_category(bank)

            if category is None:
                continue

            questions = bank.pick(ROUNDS, category=category)

            player1 = input("نام بازیکن اول: ").strip() or "بازیکن 1"
            player2 = input("نام بازیکن دوم: ").strip() or "بازیکن 2"

            play_match(questions, player1, player2)

        elif choice == "2":
            show_leaderboard(board)
            break

        else:
            console.print(
                "لطفاً گزینه ۱ یا ۲ را انتخاب کن.",
                style="yellow",
            )


if __name__ == "__main__":
    main()           