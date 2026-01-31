@echo off
set GEMINI_API_KEY=AIzaSyD9Xfq7lfErfaNOOzFjw2LQ3sAsLCZBkKg
set PYTHONUNBUFFERED=1
python tests/test_ssot_full_compliance.py --gemini-all
