# Addressbook API

A FastAPI-based address book application with SQLite storage and distance-based queries.

## Run Instructions

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Then open Swagger:
http://127.0.0.1:8000/docs
