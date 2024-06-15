from PIL import Image
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend
import os

# Function to load image and convert it to bytes
def load_image(image_path):
    with Image.open(image_path) as img:
        img = img.convert("RGB")
        return img.tobytes(), img.size

# Function to encrypt data
def encrypt_image(data, key, iv):
    # Initialize the cipher
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()

    # Pad the data to be AES block size (16 bytes)
    padder = padding.PKCS7(algorithms.AES.block_size).padder()
    padded_data = padder.update(data) + padder.finalize()

    # Encrypt the padded data
    encrypted_data = encryptor.update(padded_data) + encryptor.finalize()
    return encrypted_data

# Function to save encrypted data as image
def save_encrypted_image(data, size, output_path):
    img = Image.frombytes("RGB", size, data)
    img.save(output_path)

# Main function
def main():
    # Load image
    image_path = 'input_image.png'
    image_data, image_size = load_image(image_path)

    # Generate a random key and IV
    key = os.urandom(32)  # AES-256
    iv = os.urandom(16)   # AES block size

    # Encrypt image data
    encrypted_data = encrypt_image(image_data, key, iv)

    # Save encrypted image
    output_path = 'encrypted_image.png'
    save_encrypted_image(encrypted_data, image_size, output_path)

    # Save key and IV securely (for demonstration purposes, printing here)
    print(f"Key: {key.hex()}")
    print(f"IV: {iv.hex()}")

if __name__ == "__main__":
    main()
