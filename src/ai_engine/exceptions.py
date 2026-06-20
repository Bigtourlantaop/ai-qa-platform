class TestGenerationError(Exception):
    """Error พื้นฐานสำหรับทุกปัญหาที่เกิดจากการ generate test case"""
    pass


class InvalidResponseFormatError(TestGenerationError):
    """เกิดขึ้นเมื่อ Claude ตอบมาไม่เป็น JSON ที่ parse ได้"""
    pass


class SchemaValidationError(TestGenerationError):
    """เกิดขึ้นเมื่อ JSON parse ได้ แต่โครงสร้างไม่ตรงตาม schema ที่ต้องการ"""
    pass