# Installation Guide

## Setup Steps

1. (Optional) Create a Python virtual environment:
   ```bash
   conda create -p venv python==3.10 -y
   ```

2. Install required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the application:
   ```bash
   streamlit run app.py
   ```

## About Virtual Environment (Step 1)

Step 1 is marked as optional because:
- If you already have Python 3.10 installed and prefer to work in your global environment, you can skip this step
- Virtual environments are recommended best practice as they:
  - Isolate project dependencies
  - Prevent conflicts between different projects
  - Make your project more reproducible
  - Make it easier to manage Python and package versions

While optional, using a virtual environment is highly recommended for development.
