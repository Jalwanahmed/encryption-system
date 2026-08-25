from text_aes.aes_text import encrypt, decrypt
from image_aes.image_utils import load_grayscale, image_to_bytes, bytes_to_image, save_grayscale

# Load a real test image
arr = load_grayscale("test_data/baboon.png")
raw_bytes, shape = image_to_bytes(arr)

# Encrypt it using your AES-GCM pipeline from Track A
passphrase = "my_passphrase"
encrypted_blob = encrypt(raw_bytes, passphrase)
print("Encrypted size:", len(encrypted_blob), "bytes (original was", len(raw_bytes), ")")

# Decrypt it back
decrypted_bytes = decrypt(encrypted_blob, passphrase)
reconstructed = bytes_to_image(decrypted_bytes, shape)

# Verify pixel-perfect match
import numpy as np
assert np.array_equal(arr, reconstructed), "Image AES round-trip failed!"
print("Image AES round-trip OK.")

# Save the decrypted result so you can visually inspect it
save_grayscale(reconstructed, "test_data/baboon_aes_decrypted.png")
print("Saved test_data/baboon_aes_decrypted.png")