from fastapi import FastAPI, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import text
from typing import List
from . import database, schemas

app = FastAPI(title="Medical Telegram Analytics API")

# 1. Top Products/Mentions
@app.get("/api/reports/top-products", response_model=List[schemas.ProductMention])
def get_top_products(limit: int = 10, db: Session = Depends(database.get_db)):
    query = text("""
        SELECT f.message_text, c.channel_name 
        FROM dbt_maireg.fct_messages f
        JOIN dbt_maireg.dim_channels c ON f.channel_key = c.channel_key
        WHERE f.message_text IS NOT NULL 
        LIMIT :limit
    """)
    result = db.execute(query, {"limit": limit}).fetchall()
    return [{"message_text": r[0], "channel_name": r[1]} for r in result]

# 2. Channel Activity (Daily Trends)
@app.get("/api/channels/{channel_name}/activity", response_model=List[schemas.ChannelActivity])
def get_channel_activity(channel_name: str, db: Session = Depends(database.get_db)):
    query = text("""
        SELECT d.full_date, COUNT(f.message_id)
        FROM dbt_maireg.fct_messages f
        JOIN dbt_maireg.dim_channels c ON f.channel_key = c.channel_key
        JOIN dbt_maireg.dim_dates d ON f.date_key = d.date_key
        WHERE c.channel_name ILIKE :name
        GROUP BY d.full_date
        ORDER BY d.full_date
    """)
    result = db.execute(query, {"name": f"%{channel_name}%"}).fetchall()
    return [{"date": str(r[0]), "message_count": r[1]} for r in result]

# 3. Message Search
@app.get("/api/search/messages", response_model=List[schemas.MessageResponse])
def search_messages(query: str = Query(..., min_length=3), db: Session = Depends(database.get_db)):
    sql = text("""
        SELECT message_id, message_text, view_count 
        FROM dbt_maireg.fct_messages 
        WHERE message_text ILIKE :q 
        LIMIT 20
    """)
    result = db.execute(sql, {"q": f"%{query}%"}).fetchall()
    return [{"message_id": r[0], "message_text": r[1], "views": r[2]} for r in result]

# 4. Visual Content Stats (YOLO Results)
@app.get("/api/reports/visual-content", response_model=List[schemas.VisualStat])
def get_visual_stats(db: Session = Depends(database.get_db)):
    query = text("""
        SELECT image_category, COUNT(*) 
        FROM dbt_maireg.fct_image_detections 
        GROUP BY image_category
    """)
    result = db.execute(query).fetchall()
    return [{"image_category": r[0], "count": r[1]} for r in result]