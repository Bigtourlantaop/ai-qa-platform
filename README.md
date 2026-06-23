# 🤖 AI-Powered Intelligent Test Automation Platform

[![Run Tests](https://github.com/Bigtourlantaop/ai-qa-platform/actions/workflows/test.yml/badge.svg)](https://github.com/Bigtourlantaop/ai-qa-platform/actions/workflows/test.yml)
![Python](https://img.shields.io/badge/Python-3.12-blue)
![Playwright](https://img.shields.io/badge/Playwright-1.45-green)
![FastAPI](https://img.shields.io/badge/FastAPI-0.111-teal)
![Docker](https://img.shields.io/badge/Docker-ready-blue)

An AI-powered QA automation platform that uses **Claude API (LLM)** to automatically generate test cases, write Playwright test code, and analyze test failures — reducing manual QA effort significantly.

---

## ✨ Key Features

### 1. 🧠 AI Test Case Generator
- Converts user stories/requirements into structured test cases using Claude API
- Generates both positive, negative, and edge case scenarios automatically
- Validates output with Pydantic schema enforcement

### 2. ⚡ Auto Code Writer
- Transforms test cases (JSON) into executable Playwright + pytest code
- Saves generated test files automatically to `tests/generated/`
- Uses page context (real selectors) to ensure accurate code generation

### 3. 🔍 AI Failure Analyst
- Analyzes failed test error messages using LLM
- Categorizes root cause into: `test_code_bug`, `environment_issue`, `flaky_test`, `requirement_mismatch`
- Provides human-readable explanation and suggested fix with confidence score

---

## 🏗️ Architecture

```
User Story (text)
      ↓
TestCaseGenerator (Claude API + Pydantic validation)
      ↓
TestCase JSON (structured, validated)
      ↓
CodeWriter (Claude API + template)
      ↓
Playwright .py files (auto-saved to tests/generated/)
      ↓
pytest runner → pass ✅ / fail ❌
      ↓ (on failure)
FailureAnalyst (Claude API)
      ↓
Root cause analysis + suggested fix
```

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Test Framework | Playwright + pytest |
| AI / LLM | Anthropic Claude API (claude-sonnet-4-6) |
| Data Validation | Pydantic v2 |
| Backend API | FastAPI + Uvicorn |
| Containerization | Docker (official Playwright image) |
| CI/CD | GitHub Actions |
| Reporting | Allure Report |
| Language | Python 3.12 |

---

## 🚀 Quick Start

### Prerequisites
- Python 3.12+
- Docker (optional)
- Anthropic API key

### Local Setup

```bash
# Clone the repository
git clone https://github.com/Bigtourlantaop/ai-qa-platform.git
cd ai-qa-platform

# Create virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Mac/Linux

# Install dependencies
pip install -r requirements.txt
playwright install chromium

# Set up environment variables
echo "ANTHROPIC_API_KEY=your_api_key_here" > .env
```

### Run Tests

```bash
# Run Playwright login tests
pytest tests/unit/test_login.py -v

# Run AI generator tests
pytest tests/unit/test_generator.py -v

# Run all tests with Allure report
pytest tests/unit/test_login.py --alluredir=allure-results
allure serve allure-results
```

### Start API Server

```bash
uvicorn src.api.main:app --reload
# Open http://127.0.0.1:8000/docs
```

### Docker

```bash
docker build -t ai-qa-platform .
docker run -p 8000:8000 --env-file .env ai-qa-platform
```

---

## 📡 API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | Health check |
| GET | `/health` | Server status |
| POST | `/generate-tests` | Generate test cases + code from user story |

### Example Request

```bash
curl -X POST http://localhost:8000/generate-tests \
  -H "Content-Type: application/json" \
  -d '{"user_story": "As a user, I want to log in with email and password."}'
```

---

## ⚠️ Known Limitations & Future Improvements

- **File naming**: Generated test files use TC ID as filename (`test_tc_001.py`) — later runs overwrite earlier ones. Fix: add timestamp/UUID to filename.
- **Page context**: Currently hardcoded for saucedemo.com login page. Future: auto-scan DOM to extract selectors dynamically.
- **AI hallucination**: LLM occasionally generates incorrect Playwright API usage (e.g., passing lambda to `to_have_url()`). Mitigation: Failure Analyst detects and categorizes these automatically.

---

## 📊 Test Results

- **test_login.py**: 3/3 passed ✅ (manual tests, Page Object Model)
- **tests/generated/**: 9/11 passed (AI-generated tests, 2 known failures preserved for demo)
- **CI/CD**: Auto-runs on every push to `main` via GitHub Actions