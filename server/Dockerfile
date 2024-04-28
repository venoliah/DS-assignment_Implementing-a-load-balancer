FROM python:3.9

WORKDIR /app

# Copy the requirements file to the working directory
COPY requirements.txt .

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the server code to the working directory
COPY server.py .

COPY consistent_hash.py .

# Run the server when the container starts
CMD ["uvicorn", "server:app", "--host", "0.0.0.0"]