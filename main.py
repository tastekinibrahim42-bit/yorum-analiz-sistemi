from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import sqlite3
import json

app = FastAPI(title="Yorum Analiz API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

DB_PATH = "reviews_database.db"

@app.get("/api/reports")
def get_latest_report(city: str = Query("Antalya"), sector: str = Query("kasap")):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT analysis_json, updated_at FROM analysis_reports ORDER BY id DESC LIMIT 1')
    row = cursor.fetchone()
    conn.close()
    if not row:
        return {"error": "Veri bulunamadı"}
    data = json.loads(row[0])
    data["updated_at"] = row[1]
    return data

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
