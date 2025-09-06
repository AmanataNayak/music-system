from sqlalchemy.orm import Session
from sqlalchemy import text

def search_full_text(db: Session, query: str) -> list:
    sql = text("""
        SELECT id, title, 'song' AS type
        FROM songs
        WHERE to_tsvector('english', title) @@ plainto_tsquery(:q)
        UNION
        SELECT id, title, 'album' AS type
        FROM albums
        WHERE to_tsvector('english', title) @@ plainto_tsquery(:q)
        UNION
        SELECT id, name AS title, 'artist' AS type
        FROM artists
        WHERE to_tsvector('english', name) @@ plainto_tsquery(:q)
        LIMIT 50;
    """)
    results = db.execute(sql, {"q": query}).fetchall()
    return [{"type": r.type, "id": str(r.id), "title": r.title} for r in results]

def get_track(db: Session, track_id: str):
    # Join songs -> albums -> artists
    query = text("""
    SELECT Songs.id, Songs.title, Songs.duration, language, Songs.release_date, album_id, 
        Albums.title as album_title, Songs.artist_id, Artists.name as artist_name
        FROM Songs JOIN Artists on Songs.artist_id = Artists.id
        LEFT OUTER JOIN Albums on Songs.album_id = Albums.id
        WHERE Songs.id = :track_id
    """)
    track = db.execute(query, {"track_id": track_id}).first()
    return track
