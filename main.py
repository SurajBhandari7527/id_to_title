from fastapi import FastAPI, HTTPException
import csv
import os

app = FastAPI()

# Global dictionary to store the mapping
# Structure: 
# {
#   'tt1234567': {
#       'title': 'Batman', 
#       'cast': 'Actor A, Actor B', 
#       'poster_path': 'https://...'
#    }
# }
movie_db = {}

@app.on_event("startup")
def load_data():
    filename = "imdb_id_to_title.csv"
    print(f"Loading {filename} into memory...")
    
    if not os.path.exists(filename):
        print(f"CRITICAL ERROR: {filename} not found!")
        return

    try:
        with open(filename, mode="r", encoding="utf-8") as f:
            # vital: CSV must have headers like: imdb_id,title,cast,poster_path
            reader = csv.DictReader(f)
            
            count = 0
            for row in reader:
                # robust extraction (handles missing columns gracefully)
                if 'imdb_id' in row:
                    imdb_id = row['imdb_id'].strip()
                    
                    # Store as a lightweight dictionary
                    movie_db[imdb_id] = {
                        "title": row.get('title', '').strip(),
                        "cast": row.get('cast', '').strip(),
                        "poster_path": row.get('poster_path', '').strip()
                    }
                    count += 1
            
            print(f"Success! Loaded {count} movies into memory.")
            
    except Exception as e:
        print(f"Error reading CSV: {e}")

@app.get("/")
def home():
    return {"message": "Movie Details Service is running."}

@app.get("/get_title")
def get_movie_details(imdb_id: str):
    """
    Endpoint: Returns title, cast, and poster_path for a given IMDB ID.
    """
    # O(1) lookup speed
    movie_data = movie_db.get(imdb_id)
    
    if not movie_data:
        raise HTTPException(status_code=404, detail="ID not found in database")
    
    # Construct the response
    return {
        "imdb_id": imdb_id,
        "title": movie_data['title'],
        "cast": movie_data['cast'],
        "poster_path": movie_data['poster_path']
    }