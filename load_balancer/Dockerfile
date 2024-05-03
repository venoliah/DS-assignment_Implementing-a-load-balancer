FROM python:3.9

WORKDIR /app

# Install Python packages using pip
RUN pip install fastapi uvicorn docker

# Copy the requirements file to the working directory
COPY requirements.txt .

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the load balancer code to the working directory
COPY load_balancer.py .

COPY consistent_hash.py .

# Expose the port on which the load balancer will run (e.g., port 800)
EXPOSE 8080

# Run the load balancer when the container starts
CMD ["uvicorn", "load_balancer:app", "--host", "0.0.0.0", "--port", "8080"]