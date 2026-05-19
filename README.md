# Calculator App — CI/CD Pipeline Demo

A simple Python project demonstrating a full CI/CD pipeline using Jenkins + GitHub.

## Project Structure

```
cicd-project/
├── app/
│   └── calculator.py       # Main application
├── tests/
│   └── test_calculator.py  # Pytest unit tests (15 tests)
├── requirements.txt        # Python dependencies
├── Jenkinsfile             # CI/CD pipeline definition
└── README.md
```

## Pipeline Stages

| Stage    | What happens |
|----------|-------------|
| Checkout | Jenkins pulls latest code from GitHub |
| Build    | Creates Python venv, installs dependencies, runs app |
| Test     | Runs 15 pytest tests, generates HTML report |
| Deploy   | Copies app to deploy directory, creates manifest, smoke test |

## Run Locally

```bash
# Install dependencies
pip install -r requirements.txt

# Run app
python app/calculator.py

# Run tests
pytest tests/ -v --html=test-report.html
```

## Jenkins Setup

1. Install Jenkins locally or use a server
2. Push this project to GitHub
3. Create a new Pipeline job in Jenkins
4. Set SCM to Git → your GitHub repo URL
5. Jenkins auto-detects the Jenkinsfile
6. Click **Build Now** → watch the pipeline run!
