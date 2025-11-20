# Use a lightweight Python image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy requirements
COPY requirements.txt .

# Install dependencies (No pandas/numpy needed, so this is very fast)
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code and the CSV
COPY . .

# Expose the port
EXPOSE 10000

# Start the app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "10000"]