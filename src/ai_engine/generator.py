import os
import json
import logging
from anthropic import Anthropic
from pydantic import ValidationError

from src.ai_engine.prompts import SYSTEM_PROMPT, build_test_case_prompt
from src.ai_engine.schemas import TestCaseList
from src.ai_engine.exceptions import InvalidResponseFormatError, SchemaValidationError

logger = logging.getLogger(__name__)


class TestCaseGenerator:
    """
    ใช้ Claude API เพื่อแปลง user story เป็น test case ที่มี schema ชัดเจน
    มี retry logic ในกรณีที่ Claude ตอบ format ผิดในบางครั้ง
    """

    def __init__(self, api_key: str | None = None, max_retries: int = 2):
        self.client = Anthropic(api_key=api_key or os.getenv("ANTHROPIC_API_KEY"))
        self.max_retries = max_retries
        self.model = "claude-sonnet-4-6"

    def generate(self, user_story: str) -> TestCaseList:
        """
        สร้าง test case จาก user story
        คืนค่าเป็น TestCaseList (validated Pydantic object)
        raise TestGenerationError ถ้าล้มเหลวครบจำนวน retry แล้ว
        """
        last_error: Exception | None = None

        for attempt in range(1, self.max_retries + 1):
            try:
                raw_text = self._call_claude(user_story)
                parsed_json = self._parse_json(raw_text)
                validated = self._validate_schema(parsed_json)
                logger.info(
                    "Generated %d test cases (attempt %d)",
                    len(validated.test_cases), attempt
                )
                return validated

            except InvalidResponseFormatError as e:
                last_error = e
                logger.warning("Attempt %d: invalid JSON format - %s", attempt, e)

            except SchemaValidationError as e:
                last_error = e
                logger.warning("Attempt %d: schema validation failed - %s", attempt, e)

        raise last_error

    def _call_claude(self, user_story: str) -> str:
        """เรียก Claude API และคืนค่า raw text response"""
        response = self.client.messages.create(
            model=self.model,
            max_tokens=4096,
            temperature=0.3,
            system=SYSTEM_PROMPT,
            messages=[
                {"role": "user", "content": build_test_case_prompt(user_story)}
            ]
        )
        return response.content[0].text

    def _parse_json(self, raw_text: str) -> dict:
        """พยายาม parse raw text เป็น JSON dict"""
        try:
            return json.loads(raw_text)
        except json.JSONDecodeError as e:
            raise InvalidResponseFormatError(
                f"ไม่สามารถ parse JSON ได้: {e}"
            ) from e

    def _validate_schema(self, parsed_json: dict) -> TestCaseList:
        """ตรวจสอบว่า JSON ตรงตาม schema ที่กำหนดไว้"""
        try:
            return TestCaseList(**parsed_json)
        except ValidationError as e:
            raise SchemaValidationError(
                f"JSON ไม่ตรงตาม schema: {e}"
            ) from e