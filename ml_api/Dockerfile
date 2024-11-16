FROM python:3.10.12-slim


WORKDIR /app

# Needed for running psycopg2
RUN apt-get update && \
	apt-get install -y postgresql-server-dev-all gcc && \
	apt-get clean

# Install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy app code
COPY . .

# Expose app port
EXPOSE 8000

# Run app on port 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
