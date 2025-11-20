from fastapi import FastAPI, HTTPException
import csv
import os

app = FastAPI()

id_to_title_db = {}

@app.on_event("startup")
def load_data():
    filename = "imdb_id_to_title.csv"
    print(f"Loading {filename} into memory...")
    
    if not os.path.exists(filename):
        print(f"CRITICAL ERROR: {filename} not found!")
        return

    try:
        with open(filename, mode="r", encoding="utf-8") as f:
            # Assuming the CSV has headers: imdb_id,title
            reader = csv.DictReader(f)
            
            count = 0
            for row in reader:
                # Clean keys just in case of whitespace
                if 'imdb_id' in row and 'title' in row:
                    imdb_id = row['imdb_id'].strip()
                    title = row['title'].strip()
                    id_to_title_db[imdb_id] = title
                    count += 1
            
            print(f"Success! Loaded {count} titles into memory.")
            
    except Exception as e:
        print(f"Error reading CSV: {e}")

@app.get("/")
def home():
    return {"message": "IMDB ID to Title Service is running."}

@app.get("/get_title")
def get_title(imdb_id: str):
    """
    Endpoint: Returns the title for a given IMDB ID.
    """
    # O(1) lookup speed
    title = id_to_title_db.get(imdb_id)
    
    if not title:
        raise HTTPException(status_code=404, detail="ID not found in database")
    
    return {
        "imdb_id": imdb_id,
        "title": title
    }