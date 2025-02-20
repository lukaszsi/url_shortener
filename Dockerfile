# Use a slim Python 3.10 image
FROM python:3.10-slim

# Prevent Python from writing .pyc files and enable unbuffered output
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set working directory in the container
WORKDIR /app

# Install system dependencies (if needed)
RUN apt-get update && apt-get install -y build-essential

# Install Poetry
RUN pip install poetry

# Copy Poetry configuration files first to leverage Docker cache
COPY pyproject.toml poetry.lock /app/

# Configure Poetry to install dependencies globally (i.e. no virtualenv)
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi

# Copy the rest of the project files
COPY . /app/

# Expose port 8000 for the Django development server
EXPOSE 8000

# Run migrations then start the Django development server
CMD ["sh", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]
