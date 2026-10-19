"""
Main entry point for AI Tech Consultant Platform.
Proxies to the unified Master Enterprise App (app.py).
"""

from app import app

if __name__ == "__main__":
    import uvicorn
    print("\n -> Master Web App: http://localhost:8000\n")
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=False)
