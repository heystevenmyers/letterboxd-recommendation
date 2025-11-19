"""
Vercel Entry Point
This file imports the Flask app from backend/app.py
Vercel will automatically detect this as the Flask application entrypoint
"""
from backend.app import app

# Export the app instance for Vercel
__all__ = ['app']

