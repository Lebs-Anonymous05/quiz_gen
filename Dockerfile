# Use official Python image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install dependencies
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend code
COPY backend/ .

# Expose port
EXPOSE 5000

# Run the app with gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "run:app"]