from typing import List
from datetime import datetime, timedelta

from server.apps.learn.models import AnswerHistory


def sm2(
    x: List[AnswerHistory],
    *,
    a: float = 6.0,
    b: float = -0.8,
    c: float = 0.28,
    d: float = 0.02,
    theta: float = 0.2,
) -> float:
    """
    Returns the number of days to delay the next review of an item by,
    fractionally, based on the history of answers x to
    a given question, where
    x == 0: Incorrect, Hardest
    x == 1: Incorrect, Hard
    x == 2: Incorrect, Medium
    x == 3: Correct, Medium
    x == 4: Correct, Easy
    x == 5: Correct, Easiest
    @param x The history of answers in the above scoring.
    @param theta When larger, the delays for correct answers will increase.
    @param a coefficients
    @param b coefficients
    @param c coefficients
    @param d coefficients
    """
    assert all(0 <= x_i.answer <= 5 for x_i in x)
    correct_x = [x_i.answer >= 3 for x_i in x]
    # If you got the last question incorrect, just return 1
    if not correct_x[-1]:
        return 1.0

    # Calculate the latest consecutive answer streak
    num_consecutively_correct = 0
    for correct in reversed(correct_x):
        if correct:
            num_consecutively_correct += 1
        else:
            break

    return a * (max(1.3, 2.5 + sum(
        b + c * x_i.answer + d * x_i.answer * x_i.answer for x_i in x
    ))) ** (theta * num_consecutively_correct)


def get_next_repeat(answers_history: List[AnswerHistory]) -> datetime:
    now = datetime.now()
    return now + timedelta(sm2(answers_history))
