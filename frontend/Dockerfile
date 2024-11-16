FROM python:3.10.12-slim

WORKDIR /app

RUN pip install streamlit

# Copy app code
COPY . .

# Expose Streamlit port
EXPOSE 9000

# Run Streamlit app on port 9000
CMD ["streamlit", "run", "frontend.py", "--server.port", "9000", "--server.address", "0.0.0.0"]