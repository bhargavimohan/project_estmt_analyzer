# Project Estmt Analyzer

## Overview
Project Estmt Analyzer is a FastAPI-based application for uploading and analyzing credit card statements. Please note that this is a personal/family project, and it currently works only with my own credit card statements or for users who are using the service provided by [Gebührenfrei]

## Features
- Upload PDF files for analysis
- Validate file types to ensure only PDFs are accepted
- Process and analyze the content of the PDFs
- Store analysis results in a database
- Retrieve the list of analyzed PDFs

### Limitations

Please note that the application is currently implemented to work with credit card statements from users of [Gebührenfrei]. It does not support other credit card providers or formats. 

## Installation

### Prerequisites
- Python 3.12
- Docker

## Running the Application

### Using Docker

1. **Build the Docker Image**

```bash
docker build --no-cache -t project_estmt_analyzer .
```

2. **Run the docker image**

```bash
docker run -p 8002:8002 project_estmt_analyzer
```

### Without Docker

1. **Install Dependencies**

```bash
pip install -r requirements.txt
```

2. **Navigate to the src folder**

```bash
uvicorn server:app --host 0.0.0.0 --port 8002
```

## Testing the Application

The application uses `pytest` for testing, and there are two test modules:

1. **Run the tests using pytest**
```bash
pytest path/to/a/test_module.py
```
2. **Server Test Module** - Tests for the FastAPI server endpoints.
3. **Processing Test Module** - Tests for the credit card statement processing functionality.



