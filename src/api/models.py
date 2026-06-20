from pydantic import BaseModel, Field
from src.ai_engine.schemas import TestCase


class GenerateTestsRequest(BaseModel):
    """รูปแบบข้อมูลที่ client ต้องส่งมา"""
    user_story: str = Field(
        min_length=10,
        max_length=1000,
        description="User story หรือ requirement ที่ต้องการสร้าง test case"
    )


class GenerateTestsResponse(BaseModel):
    """รูปแบบข้อมูลที่ API ตอบกลับ"""
    success: bool
    test_cases: list[TestCase]
    generated_files: list[str]
    total_count: int


class ErrorResponse(BaseModel):
    """รูปแบบข้อมูลเมื่อเกิด error"""
    success: bool = False
    error: str
    detail: str | None = None