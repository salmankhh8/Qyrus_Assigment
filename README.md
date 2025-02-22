# Chat Code-Interpreter Backend

This is a **FastAPI-based** backend that acts as a code interpreter. It allows users to upload CSV files and request data analysis or computations. The backend generates Python code using OpenAI's GPT model, executes the code, and returns results.

---

## Features
- Upload CSV files for processing.
- Uses OpenAI GPT (`gpt-3.5-turbo`) to generate Python scripts dynamically.
- Executes generated Python scripts securely.
- Supports natural language queries (e.g., *"Find the average sales from this file."*).
- Supports both REST API & Docker deployment.
- API Key authentication via environment variables.
- Built with **FastAPI**, **Uvicorn**, and **OpenAI API**.
- Dockerized for easy deployment.

---

## Installation & Setup
### Prerequisites
- **Python 3.12+**
- **pip** (Python package manager)
- **Docker (optional for containerization)**

---

### 1. Install Dependencies
Clone the repository and install required Python packages:

```bash
git clone https://github.com/your-repo/chat-code-interpreter.git
cd chat-code-interpreter
pip install -r requirements.txt

