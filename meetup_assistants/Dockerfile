FROM python:3.12-alpine

# Install dependencies
RUN apk update && apk add --no-cache libpq postgresql-dev gcc musl-dev linux-headers

# Set working directory
WORKDIR /app

# Copy requirements.txt and install Python dependencies
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# Copy the rest of the application code
COPY . /app

# Set the PYTHONPATH to ensure all modules can be found
ENV PYTHONPATH=/app/app

# Command to run your application using Uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--log-level", "info"]
