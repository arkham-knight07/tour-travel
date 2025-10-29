import os

# backend root (this file is backend/utils/paths.py)
BACKEND_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT_ROOT = os.path.dirname(BACKEND_ROOT)

def backend_path(*parts):
    return os.path.join(BACKEND_ROOT, *parts)

def frontend_path(*parts):
    return os.path.join(PROJECT_ROOT, "frontend", *parts)
