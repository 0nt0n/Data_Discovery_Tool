import pytest
from backend.search import search


def test_search_empty():
    results = search("")
    assert results == []


def test_search_exact_column():
    results = search("country")
    assert len(results) > 0
    assert results[0].column == "country"


def test_search_sorted_by_score():
    results = search("country")
    assert results[0].score >= results[-1].score


def test_search_fuzzy():
    results = search("cuntry")
    assert len(results) > 0
    assert any(r.column == "country" for r in results)


def test_search_value():
    results = search("France")
    assert any(r.type == "value" for r in results)


def test_search_no_results():
    results = search("xyz123абвгд")
    assert results == []
