# API Test Automation & AI-Generated Test Case Validator

A small, portfolio-ready software quality project demonstrating API regression testing, negative testing, response validation, parameterized test cases, a CI workflow, and a validator for AI-generated test-case specifications.

## Why this is relevant
- **Automation:** pytest test suite for API endpoints.
- **Coverage:** happy paths, missing resources, malformed requests, and invalid inputs.
- **Validation:** status codes, response fields, types, and key values are checked.
- **AI-assisted workflow:** validates the structure and basic consistency of test cases produced by an AI tool or written manually. It does **not** itself call an AI model and cannot determine semantic correctness.
- **CI:** GitHub Actions runs tests on pushes and pull requests.

## Run locally
```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
pytest
python tools/validate_generated_cases.py examples/ai_generated_test_cases.json
```

## Test coverage
- Health endpoint
- Existing and missing users
- Response schema and value checks
- Successful user creation
- Missing fields, blank names, invalid email
- Non-JSON request body
- Generated test-case structure, supported HTTP methods, duplicate IDs/scenarios, and expected status format

## Suggested next steps
1. Add coverage measurement with `pytest-cov`.
2. Export JUnit XML for test reporting (`pytest --junitxml=reports/results.xml`).
3. Add contract/schema validation for larger APIs.
4. Integrate an LLM only after defining a review process and a curated expected-results dataset.
5. Replace the demo API with a project API after securing test data and credentials.

## Important
This project uses a deliberately small demo API. It is a learning/portfolio project, not production-grade security or a claim of commercial testing experience.
