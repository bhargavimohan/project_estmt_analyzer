import pytest
from tests.test_utils import (
    HELPER_PDF_TEXT,
    HELPER_COST_LIST,
    HELPER_CLASSIFIED_COSTS_DICT,
    HELPER_FINAL_COSTS_DICT,
)
from src.review_pdf import (
    read_pdf,
    extract_desired_costs,
    classify_costs,
    compute_category_costs,
    verify_category_total_costs,
)


TEST_PDF = "pdfs/test_estmt.pdf"


def test_read_pdf():
    text = read_pdf(TEST_PDF)
    assert isinstance(text, str)
    assert len(text) > 0


def test_extract_desired_costs():
    pdf_text = HELPER_PDF_TEXT
    costs = extract_desired_costs(pdf_text)
    assert isinstance(costs, list)
    assert len(costs) == 47  # 47 costs in the test PDF


def test_classify_costs():
    cost_list = HELPER_COST_LIST
    classified_costs = classify_costs(cost_list)
    assert isinstance(classified_costs, dict)
    assert (
        classified_costs["Old Balance"] == "ALTER SALDO 1.115,73"
    )  # values from test PDF
    assert (
        classified_costs["New Balance"] == "03.01.2025 NEUER SALDO 699,51"
    )  # values from test PDF
    assert len(classified_costs) == 11  # length of the dictionary


def test_compute_category_costs():
    classified_costs = HELPER_CLASSIFIED_COSTS_DICT
    final_costs = compute_category_costs(classified_costs)
    assert isinstance(final_costs, dict)


def test_verify_category_total_costs():
    final_costs = HELPER_FINAL_COSTS_DICT
    verified_costs = verify_category_total_costs(final_costs)
    assert isinstance(verified_costs, dict)
    assert verified_costs["New Balance"] == verified_costs["Cost of ALL categories"]
