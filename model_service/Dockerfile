FROM python:3.10.12-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy app code
COPY . .

VOLUME /app/data

# Run app on port 8000
CMD ["python", "main.py"]
