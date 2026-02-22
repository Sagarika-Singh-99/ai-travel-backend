# Use official Python 3.12 slim image (lightweight)
FROM python:3.12-slim

# Set working directory inside the container
WORKDIR /app

# Copy dependency list first (for faster rebuilds)
COPY requirements.txt .

# Install all Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the backend code
COPY . .

# Expose port 8000 so other containers can reach it
EXPOSE 8000

# Start FastAPI with Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]




# Line	What it does
# FROM python:3.12-slim	Starts with a clean lightweight Python environment
# WORKDIR /app	All commands run from this folder inside the container
# COPY requirements.txt .	Copies dependency list before code (Docker cache trick)
# RUN pip install	Installs all dependencies
# COPY . .	Copies your actual code
# EXPOSE 8000	Documents which port the app uses
# CMD ["uvicorn"...]	The command that starts your server


