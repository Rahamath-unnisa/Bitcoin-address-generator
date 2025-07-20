import sqlite3

def create_db():
    conn = sqlite3.connect("bitshala.db")
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS keys
                 (username TEXT PRIMARY KEY, private_key TEXT, public_key TEXT, address TEXT)''')
    conn.commit()
    conn.close()

def store_keys(data):
    conn = sqlite3.connect("bitshala.db")
    c = conn.cursor()

    # Check if username exists
    c.execute("SELECT * FROM keys WHERE username=?", (data["username"],))
    result = c.fetchone()

    if result:
        conn.close()
        return False  # Username exists

    c.execute("INSERT INTO keys VALUES (?, ?, ?, ?)", 
              (data["username"], data["private_key"], data["public_key"], data["address"]))
    conn.commit()
    conn.close()
    return True
