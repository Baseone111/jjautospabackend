FROM python:3.11-slim

WORKDIR /usr/src/app

# Install system dependencies
RUN apt-get update && apt-get install -y default-libmysqlclient-dev build-essential && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy everything
COPY . .

# Add the current directory to PYTHONPATH so Python can see the modules
ENV PYTHONPATH=/usr/src/app

# Try to run it using the module path
CMD ["uvicorn", "app.src.main:app", "--host", "0.0.0.0", "--port", "8000"]