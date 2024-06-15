from PIL import Image
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend

# Function to load encrypted image and convert it to bytes
def load_encrypted_image(image_path):
    with Image.open(image_path) as img:
        img = img.convert("RGB")
        return img.tobytes(), img.size

# Function to decrypt data
def decrypt_image(data, key, iv):
    # Initialize the cipher
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()

    # Decrypt the data
    decrypted_data = decryptor.update(data) + decryptor.finalize()

    # Unpad the data
    unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
    unpadded_data = unpadder.update(decrypted_data) + unpadder.finalize()

    return unpadded_data

# Function to save decrypted data as image
def save_decrypted_image(data, size, output_path):
    img = Image.frombytes("RGB", size, data)
    img.save(output_path)

# Main function
def main():
    # Load encrypted image
    image_path = 'encrypted_image.png'
    encrypted_data, image_size = load_encrypted_image(image_path)

    # The key and IV used for encryption (must be securely retrieved)
    key = bytes.fromhex('fcc76948ea6f0497c1928908857db707717ca5ed18ccb7b7fe8de40fe3af7a1d')
    iv = bytes.fromhex('2a6df5373f88c7e740bea07c99defd47')

    # Decrypt image data
    decrypted_data = decrypt_image(encrypted_data, key, iv)

    # Save decrypted image
    output_path = 'decrypted_image.png'
    save_decrypted_image(decrypted_data, image_size, output_path)

    print(f"Image decrypted and saved to {output_path}")

if __name__ == "__main__":
    main()
