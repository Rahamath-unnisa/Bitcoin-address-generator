from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import sqlite3

app = FastAPI()

# 🔧 Initialize SQLite database and create table if not exists
def init_db():
    conn = sqlite3.connect("bitcoin.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS keys (
            username TEXT PRIMARY KEY,
            password TEXT,
            private_key TEXT,
            public_key TEXT,
            address TEXT
        )
    """)
    conn.commit()
    conn.close()

# Call DB initializer on app startup
init_db()

# 📦 Request models for input validation using Pydantic
class KeyData(BaseModel):
    username: str
    password: str
    private_key: str
    public_key: str
    address: str

class VerifyRequest(BaseModel):
    username: str
    password: str

# ✅ Store new user's keys
@app.post("/store_keys/")
def store_keys(data: KeyData):
    try:
        normalized_username = data.username.strip().lower()
        conn = sqlite3.connect("bitcoin.db")
        cursor = conn.cursor()

        # Check if username already exists
        cursor.execute("SELECT * FROM keys WHERE username = ?", (normalized_username,))
        existing = cursor.fetchone()

        if existing:
            conn.close()
            raise HTTPException(status_code=409, detail="User already exists.")

        # Insert new keys into the table
        cursor.execute("""
            INSERT INTO keys (username, password, private_key, public_key, address)
            VALUES (?, ?, ?, ?, ?)
        """, (
            normalized_username,
            data.password,
            data.private_key,
            data.public_key,
            data.address
        ))

        conn.commit()
        conn.close()

        return {"message": "Keys stored successfully."}

    except sqlite3.IntegrityError as e:
        raise HTTPException(status_code=400, detail=f"Database integrity error: {str(e)}")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")


# 🔐 Verify user credentials and return their keys
@app.post("/verify_user/")
def verify_user(data: VerifyRequest):
    normalized_username = data.username.strip().lower()
    conn = sqlite3.connect("bitcoin.db")
    cursor = conn.cursor()

    # Fetch password and keys for the given username
    cursor.execute(
        "SELECT password, private_key, public_key, address FROM keys WHERE username = ?",
        (normalized_username,)
    )
    result = cursor.fetchone()
    conn.close()

    if result and result[0] == data.password:
        return {
            "private_key": result[1],
            "public_key": result[2],
            "address": result[3]
        }
    else:
        raise HTTPException(status_code=401, detail="Invalid credentials")


# 🔎 Check if user already exists — no password verification
@app.get("/get_keys/{username}")
def get_keys(username: str):
    normalized_username = username.strip().lower()
    conn = sqlite3.connect("bitcoin.db")
    cursor = conn.cursor()

    # Only checking for existence using private_key presence
    cursor.execute("SELECT private_key FROM keys WHERE username = ?", (normalized_username,))
    result = cursor.fetchone()
    conn.close()

    if result:
        return {"message": "User exists"}
    else:
        raise HTTPException(status_code=404, detail="User not found")
