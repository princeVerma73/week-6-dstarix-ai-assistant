import sys
from pathlib import Path

sys.path.append(
    str(Path(__file__).resolve().parent.parent)
)

from evaluation.test_cases import test_cases
from main import run_rag


def keyword_coverage(
    answer,
    expected
):

    answer_words = set(
        answer.lower().split()
    )

    expected_words = set(
        expected.lower().split()
    )

    if not expected_words:
        return 0

    matched = answer_words.intersection(
        expected_words
    )

    return (
        len(matched) /
        len(expected_words)
    )


def evaluate_answer(
    answer,
    expected
):

    coverage = keyword_coverage(
        answer,
        expected
    )

    passed = coverage >= 0.6

    return passed, coverage


def run_evaluation():

    passed = 0

    total = len(test_cases)

    for i, test_case in enumerate(
        test_cases,
        start=1
    ):

        question = test_case["question"]

        expected = test_case["expected"]

        print(f"\nTest {i}")

        print(
            f"Question: {question}"
        )

        answer = run_rag(
            question
        )

        success, score = evaluate_answer(
            answer,
            expected
        )

        print(
            f"Answer: {answer}"
        )

        print(
            f"Keyword Coverage: {score:.2f}"
        )

        if success:

            print("PASS")

            passed += 1

        else:

            print("FAIL")


    accuracy = (
        passed / total * 100
        if total > 0
        else 0
    )

    print("\nEvaluation Summary")

    print(
        f"Passed: {passed}/{total}"
    )

    print(
        f"Accuracy: {accuracy:.2f}%"
    )


if __name__ == "__main__":

    run_evaluation()