"""
HTML/URL to PDF Microservice
A simple API that converts URLs or HTML content to PDF files.
"""

import os
import asyncio
from fastapi import FastAPI, HTTPException, Depends, Header
from fastapi.responses import Response
from pydantic import BaseModel, HttpUrl
from typing import Optional
from playwright.async_api import async_playwright

app = FastAPI(
    title="HTML to PDF Microservice",
    description="Convert URLs or HTML content to PDF",
    version="1.0.0"
)

# Get API token from environment variable
API_TOKEN = os.getenv("API_TOKEN", "changeme")


def verify_token(authorization: str = Header(...)):
    """Verify the Bearer token."""
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid authorization header")
    token = authorization[7:]  # Remove "Bearer " prefix
    if token != API_TOKEN:
        raise HTTPException(status_code=401, detail="Invalid token")
    return token


class URLRequest(BaseModel):
    url: HttpUrl
    
    class Config:
        json_schema_extra = {
            "example": {"url": "https://example.com"}
        }


class HTMLRequest(BaseModel):
    html: str
    
    class Config:
        json_schema_extra = {
            "example": {"html": "<html><body><h1>Hello World</h1></body></html>"}
        }


async def generate_pdf_from_url(url: str) -> bytes:
    """Generate PDF from a URL."""
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        await page.goto(url, wait_until="networkidle")
        pdf_bytes = await page.pdf(format="A4", print_background=True)
        await browser.close()
        return pdf_bytes


async def generate_pdf_from_html(html: str) -> bytes:
    """Generate PDF from HTML content."""
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        await page.set_content(html, wait_until="networkidle")
        pdf_bytes = await page.pdf(format="A4", print_background=True)
        await browser.close()
        return pdf_bytes


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}


@app.post("/convert/url")
async def convert_url_to_pdf(request: URLRequest, token: str = Depends(verify_token)):
    """Convert a URL to PDF."""
    try:
        pdf_bytes = await generate_pdf_from_url(str(request.url))
        return Response(
            content=pdf_bytes,
            media_type="application/pdf",
            headers={"Content-Disposition": "attachment; filename=output.pdf"}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to convert URL: {str(e)}")


@app.post("/convert/html")
async def convert_html_to_pdf(request: HTMLRequest, token: str = Depends(verify_token)):
    """Convert HTML content to PDF."""
    try:
        pdf_bytes = await generate_pdf_from_html(request.html)
        return Response(
            content=pdf_bytes,
            media_type="application/pdf",
            headers={"Content-Disposition": "attachment; filename=output.pdf"}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to convert HTML: {str(e)}")
