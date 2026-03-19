# Use a slim Python image for a smaller footprint
FROM python:3.11-slim

WORKDIR /app

# Install the package in editable mode or just install requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the source code
COPY . .
RUN pip install .

# Expose the default port
EXPOSE 8888

# Run the server
CMD ["ccideas-mcp", "--host", "0.0.0.0", "--port", "8888"]
