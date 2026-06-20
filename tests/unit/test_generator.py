import pytest
from src.ai_engine.generator import TestCaseGenerator
from src.ai_engine.schemas import TestCaseList


def test_generate_returns_valid_test_case_list():
    """ทดสอบว่า generator เรียก Claude จริงและได้ผลลัพธ์ที่ valid"""
    generator = TestCaseGenerator()
    user_story = "As a user, I want to log in with my email and password."

    result = generator.generate(user_story)

    assert isinstance(result, TestCaseList)
    assert len(result.test_cases) >= 1

    # เช็คว่ามีทั้ง positive และ negative case
    categories = {tc.category for tc in result.test_cases}
    assert "positive" in categories
    assert "negative" in categories


def test_generate_test_case_has_required_fields():
    """ทดสอบว่าทุก test case มี field ที่จำเป็นครบ และไม่ว่างเปล่า"""
    generator = TestCaseGenerator()
    user_story = "As a user, I want to reset my password via email."

    result = generator.generate(user_story)

    for tc in result.test_cases:
        assert tc.id
        assert tc.title
        assert len(tc.steps) > 0
        assert tc.expected_result