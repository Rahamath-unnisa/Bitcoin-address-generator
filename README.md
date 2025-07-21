# Bitcoin Address Generator with GUI & API

This project is a full-stack Bitcoin address generator built using Python. It allows users to generate Bitcoin-style addresses using elliptic curve cryptography, store their keys securely, and retrieve them via a graphical interface or API.

---

## Features

- Generates Bitcoin-style addresses using ECC (secp256r1)
- Compresses public keys with Base58Check encoding
- GUI built with Tkinter (desktop interface)
- FastAPI backend for secure key storage and retrieval
- SQLite database integration
- Copy keys to clipboard with one click
- Password-protected key access

---

## Project Structure

Project Root
├── bitAddress.py       -> Key generation logic  
├── database.py         -> CLI-based DB functions (optional)  
├── GUI.py              -> Tkinter-based GUI  
├── main.py             -> FastAPI backend  
├── assets/             -> Background and logo images  
│   ├── bgimg.jpg  
│   └── bitcoin_logo.png  
└── README.md           -> Project documentation

---

## Technologies Used

- Python 3.x
- Tkinter (GUI)
- FastAPI (REST API)
- SQLite (Database)
- PIL / Pillow (image processing)
- tinyec (Elliptic Curve Cryptography)
- base58 (Base58Check encoding)
- hashlib, secrets, binascii

---

## How to Run

1. Clone the Repository

   git clone https://github.com/YOUR-USERNAME/bitcoin-address-generator.git  
   cd bitcoin-address-generator

2. Install Required Packages

   pip install fastapi uvicorn pillow base58 tinyec

3. Start the FastAPI Backend

   uvicorn main:app --reload

   Then visit: http://127.0.0.1:8000/docs to test API endpoints.

4. Run the GUI (in a new terminal window)

   python GUI.py

---

## API Endpoints

Method | Endpoint               | Description
-------|------------------------|------------------------------
POST   | /store_keys/           | Store new user's keys
POST   | /verify_user/          | Verify user credentials
GET    | /get_keys/{username}   | Check if user already exists

---

## Security Notes

- ECC curve used is `secp256r1` for demo purposes, not the Bitcoin standard `secp256k1`
- Passwords are stored in plain text for simplicity — not recommended for production
- HTTPS is not configured — use reverse proxy or HTTPS for production

---

## License

MIT License

---
📄 You can read the full project report with output screenshots [here](Bitcoin_Address_Generator_Report.pdf)


## Author

Rahamath Unnisa  
GitHub: https://github.com/Rahamath-unnisa

---

## Show Your Support

If you found this project helpful, please ⭐ the repo and share it!
