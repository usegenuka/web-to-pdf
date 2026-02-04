# HTML/URL to PDF Microservice

A simple microservice that converts URLs or HTML content to PDF files.

## Quick Start

### Using Docker Compose (recommended)

```bash
# Set your API token
export API_TOKEN=your-secret-token

# Build and run
docker compose up -d
```

### Using Docker

```bash
# Build
docker build -t html-to-pdf .

# Run
docker run -d -p 8000:8000 -e API_TOKEN=your-secret-token html-to-pdf
```

### Local Development

```bash
pip install -r requirements.txt
playwright install chromium

export API_TOKEN=your-secret-token
uvicorn main:app --reload
```

## API Endpoints

### Health Check

```bash
curl http://localhost:8000/health
```

### Convert URL to PDF

```bash
curl -X POST http://localhost:8000/convert/url \
  -H "Authorization: Bearer your-secret-token" \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com"}' \
  --output output.pdf
```

### Convert HTML to PDF

```bash
curl -X POST http://localhost:8000/convert/html \
  -H "Authorization: Bearer your-secret-token" \
  -H "Content-Type: application/json" \
  -d '{"html": "<html><body><h1>Hello World</h1><p>This is a test.</p></body></html>"}' \
  --output output.pdf
```

## API Documentation

Once running, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `API_TOKEN` | Bearer token for authentication | `changeme` |
