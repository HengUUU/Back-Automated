# Use official Python image
FROM python:3.11

# Set working directory
WORKDIR /app

# Copy requirements first (better for caching)
COPY requirements.txt .

# Install dependencies
RUN pip install --default-timeout=100 -r requirements.txt


# Expose FastAPI port
EXPOSE 8000

# Run FastAPI app using Uvicorn
CMD ["uvicorn", "main:api", "--host", "0.0.0.0", "--port", "8000"]
