FROM python:3.13-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

# System deps (add only if needed: gcc, libffi, etc.)
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user (IMPORTANT for production)
RUN useradd -m appuser
USER appuser

WORKDIR /app

# Install dependencies first (better cache)
COPY requirements.txt .

RUN pip install --user -r requirements.txt

ENV PATH="/home/appuser/.local/bin:$PATH"

# Copy project
COPY --chown=appuser:appuser . .

# DO NOT COPY .env INTO IMAGE (security issue)
CMD ["python", "-m", "app.bot"]
