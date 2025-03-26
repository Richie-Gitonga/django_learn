# Use the official Python runtime image
FROM python:3.13-slim AS builder 
 
# Create the app directory
RUN mkdir /bongohealth
 
# Set the working directory inside the container
WORKDIR /bongohealth
 
# Set environment variables 
# Prevents Python from writing pyc files to disk
ENV PYTHONDONTWRITEBYTECODE=1
#Prevents Python from buffering stdout and stderr
ENV PYTHONUNBUFFERED=1 
 
# Upgrade pip
RUN pip install --upgrade pip 
 
# Copy the Django project  and install dependencies
COPY requirements.txt  /bongohealth/

# run this command to install all dependencies 
RUN pip install --no-cache-dir -r requirements.txt

# Stage 2: Production stage
FROM python:3.13-slim

RUN useradd -m -r appuser && \
    mkdir /bongohealth && \
    chown -R appuser /bongohealth

# Copy the Python dependencies from the builder stage
COPY --from=builder /usr/local/lib/python3.13/site-packages/ /usr/local/lib/python3.13/site-packages/
COPY --from=builder /usr/local/bin/ /usr/local/bin/

# Set the working directory
WORKDIR /bongohealth

# Copy application code 
COPY --chown=appuser:appuser . .

# Set environment variables to optimize python
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Switch to non-root user
USER appuser

# Expose the application port
EXPOSE 8000
 
# Copy the Django project to the container
COPY . /bongohealth/

# Start the application using gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "3", "bongohealth.wsgi:application"]