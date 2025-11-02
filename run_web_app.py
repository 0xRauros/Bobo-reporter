#!/usr/bin/env python
"""
Simple script to run the Bobo Reporter web application
"""
from app import app

if __name__ == '__main__':
    print("=" * 60)
    print("Bobo Reporter Web App")
    print("=" * 60)
    print("\nStarting web server...")
    print("Open your browser and navigate to: http://localhost:5000")
    print("\nPress Ctrl+C to stop the server\n")
    app.run(debug=True, host='0.0.0.0', port=5000)

