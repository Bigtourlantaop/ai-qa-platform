import pytest
from src.ai_engine.generator import TestCaseGenerator
from src.ai_engine.code_writer import CodeWriter
from src.ai_engine.page_contexts import SAUCEDEMO_LOGIN_CONTEXT


def test_end_to_end_pipeline():
    """
    ทดสอบ pipeline เต็ม: user story -> test case (JSON) -> Playwright code (.py file)
    """
    generator = TestCaseGenerator()
    writer = CodeWriter()

    user_story = "As a user, I want to log in with valid email and password."
    test_case_list = generator.generate(user_story)

    generated_files = []
    for tc in test_case_list.test_cases:
        filepath = writer.write_to_file(tc.model_dump(), SAUCEDEMO_LOGIN_CONTEXT)
        generated_files.append(filepath)

        assert filepath.exists()
        content = filepath.read_text(encoding="utf-8")
        assert "def test_" in content
        assert "page" in content

    print(f"\nGenerated {len(generated_files)} test files:")
    for f in generated_files:
        print(f"  - {f}")