from chaotic.logistic_map import seed_from_passphrase, permute_pixels, unpermute_pixels, diffuse_pixels, undiffuse_pixels
from image_aes.image_utils import load_grayscale, image_to_bytes, bytes_to_image, save_grayscale
import numpy as np

arr = load_grayscale("test_data/baboon.png")
raw, shape = image_to_bytes(arr)
seed = seed_from_passphrase("my_passphrase")

# Encrypt: permute first, then diffuse
permuted = permute_pixels(raw, seed)
encrypted = diffuse_pixels(permuted, seed)
encrypted_image = bytes_to_image(encrypted, shape)
save_grayscale(encrypted_image, "test_data/baboon_CHAOTIC_ENCRYPTED.png")
print("Saved test_data/baboon_CHAOTIC_ENCRYPTED.png")

# Decrypt: undiffuse first, then unpermute (exact reverse order)
undiffused = undiffuse_pixels(encrypted, seed)
decrypted = unpermute_pixels(undiffused, seed)
decrypted_image = bytes_to_image(decrypted, shape)
save_grayscale(decrypted_image, "test_data/baboon_CHAOTIC_DECRYPTED.png")

assert np.array_equal(arr, decrypted_image), "Full chaotic pipeline round-trip failed!"
print("Full chaotic encryption/decryption round-trip OK.")