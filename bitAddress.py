import secrets
import hashlib
from tinyec import registry
import binascii
import base58

def address_generator(username):
    # 📍 Step 1: Generate a secure random 256-bit number
    random_number = secrets.randbits(256)

    # 📍 Step 2: Create Private Key — SHA-256 hash of the random number
    private_key = hashlib.sha256(random_number.to_bytes(32, 'big')).hexdigest()

    # 📍 Step 3: Generate Public Key using Elliptic Curve
    curve = registry.get_curve('secp256r1')  # Use 'secp256k1' for real Bitcoin
    G = curve.g  # Generator point
    pr = int(private_key, 16)  # Convert private key to integer
    pu = pr * G  # Public key point (x, y)

    # 📍 Step 4: Compress Public Key
    x_bytes = pu.x.to_bytes(32, 'big')
    prefix = b'\x02' if pu.y % 2 == 0 else b'\x03'
    pub = prefix + x_bytes
    public_key_hex = binascii.hexlify(pub).decode()

    # 📍 Step 5: Generate Address using Base58Check encoding
    public_key_bytes = bytes.fromhex(public_key_hex)

    # → SHA-256 hash
    hash1 = hashlib.sha256(public_key_bytes).digest()

    # → RIPEMD-160 hash
    ripemd160 = hashlib.new('ripemd160')
    ripemd160.update(hash1)
    hash2 = ripemd160.digest()

    # → Add version byte (0x00 for Bitcoin Mainnet)
    prefixed = b'\x00' + hash2

    # → Double SHA-256 for checksum
    checksum = hashlib.sha256(hashlib.sha256(prefixed).digest()).digest()[:4]

    # → Combine data and checksum
    payload = prefixed + checksum

    # → Base58 encode the payload to get the final address
    address = base58.b58encode(payload).decode()

    # ✅ Return all generated data
    return {
        "username": username,
        "private_key": private_key,
        "public_key": public_key_hex,
        "address": address
    }
