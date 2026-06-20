import os
import json
import logging
from anthropic import Anthropic
from pydantic import ValidationError

from src.ai_engine.prompts import FAILURE_ANALYSIS_SYSTEM_PROMPT, build_failure_analysis_prompt
from src.ai_engine.schemas import FailureAnalysis
from src.ai_engine.exceptions import InvalidResponseFormatError, SchemaValidationError

logger = logging.getLogger(__name__)


class FailureAnalyst:
    """ใช้ Claude วิเคราะห์ root cause ของ test ที่ fail"""

    def __init__(self, api_key: str | None = None):
        self.client = Anthropic(api_key=api_key or os.getenv("ANTHROPIC_API_KEY"))
        self.model = "claude-sonnet-4-6"

    def analyze(self, test_code: str, error_message: str) -> FailureAnalysis:
        """
        วิเคราะห์ test ที่ fail แล้วคืนค่าเป็น FailureAnalysis (validated)
        """
        response = self.client.messages.create(
            model=self.model,
            max_tokens=1024,
            temperature=0.2,
            system=FAILURE_ANALYSIS_SYSTEM_PROMPT,
            messages=[
                {"role": "user", "content": build_failure_analysis_prompt(test_code, error_message)}
            ]
        )

        raw_text = response.content[0].text

        try:
            parsed = json.loads(raw_text)
        except json.JSONDecodeError as e:
            raise InvalidResponseFormatError(f"ไม่สามารถ parse JSON ได้: {e}") from e

        try:
            analysis = FailureAnalysis(**parsed)
        except ValidationError as e:
            raise SchemaValidationError(f"JSON ไม่ตรงตาม schema: {e}") from e

        logger.info(
            "Analyzed failure: category=%s, confidence=%s",
            analysis.root_cause_category, analysis.confidence
        )
        return analysis