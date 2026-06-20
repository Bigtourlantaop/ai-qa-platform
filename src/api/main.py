import logging
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse

from src.api.models import GenerateTestsRequest, GenerateTestsResponse, ErrorResponse
from src.ai_engine.generator import TestCaseGenerator
from src.ai_engine.code_writer import CodeWriter
from src.ai_engine.page_contexts import SAUCEDEMO_LOGIN_CONTEXT
from src.ai_engine.exceptions import TestGenerationError

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="AI Test Automation Platform",
    description="API สำหรับสร้าง test case และโค้ด Playwright อัตโนมัติด้วย AI",
    version="1.0.0"
)

generator = TestCaseGenerator()
writer = CodeWriter()


@app.get("/")
def root():
    return {"message": "AI Test Automation Platform API", "status": "running"}


@app.get("/health")
def health_check():
    """endpoint สำหรับเช็คว่า server ยังทำงานอยู่ (มักใช้ใน CI/CD และ monitoring)"""
    return {"status": "healthy"}


@app.post("/generate-tests", response_model=GenerateTestsResponse)
def generate_tests(request: GenerateTestsRequest):
    """
    รับ user story แล้วสร้าง test case + โค้ด Playwright อัตโนมัติ
    """
    try:
        logger.info("Generating tests for user story: %s", request.user_story[:50])

        test_case_list = generator.generate(request.user_story)

        generated_files = []
        for tc in test_case_list.test_cases:
            filepath = writer.write_to_file(tc.model_dump(), SAUCEDEMO_LOGIN_CONTEXT)
            generated_files.append(str(filepath))

        return GenerateTestsResponse(
            success=True,
            test_cases=test_case_list.test_cases,
            generated_files=generated_files,
            total_count=len(generated_files)
        )

    except TestGenerationError as e:
        logger.error("Test generation failed: %s", e)
        raise HTTPException(
            status_code=500,
            detail=f"ไม่สามารถสร้าง test ได้: {str(e)}"
        )