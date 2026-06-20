from pydantic import BaseModel, Field
from typing import Literal


class TestCase(BaseModel):
    """โครงสร้างของ test case 1 ตัว"""
    id: str
    title: str
    priority: Literal["high", "medium", "low"]
    category: Literal["positive", "negative", "edge_case"]
    steps: list[str]
    expected_result: str


class TestCaseList(BaseModel):
    """โครงสร้างของ response ทั้งหมดจาก Claude"""
    test_cases: list[TestCase] = Field(min_length=1)


class FailureAnalysis(BaseModel):
    """ผลการวิเคราะห์ของ AI ว่า test fail เพราะอะไร"""
    root_cause_category: Literal[
        "test_code_bug",      # โค้ด test เขียนผิด (เช่น ใช้ API ผิด)
        "environment_issue",   # selector/page_context ไม่ครบ หรือเว็บไม่รองรับ
        "flaky_test",          # อาจเป็น timing/network ไม่แน่นอน
        "requirement_mismatch" # test case ตั้ง assumption ผิดจาก requirement จริง
    ]
    explanation: str = Field(description="คำอธิบาย root cause แบบเข้าใจง่าย")
    suggested_fix: str = Field(description="คำแนะนำวิธีแก้")
    confidence: Literal["high", "medium", "low"]