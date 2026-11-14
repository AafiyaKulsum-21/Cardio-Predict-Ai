"""
CardioPredict AI: Application Entry Point
Usage:
    python run.py
"""

from app.app import app

if __name__ == '__main__':
    print("=" * 65)
    print("      CARDIOPREDICT AI: STARTING FLASK WEB SERVER")
    print("      Open http://127.0.0.1:5000 in your browser")
    print("=" * 65)
    app.run(host='0.0.0.0', port=5000, debug=False)
