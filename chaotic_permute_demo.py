from chaotic.logistic_map import seed_from_passphrase, permute_pixels, unpermute_pixels
from image_aes.image_utils import load_grayscale, image_to_bytes, bytes_to_image, save_grayscale
import numpy as np

arr = load_grayscale("test_data/baboon.png")
raw, shape = image_to_bytes(arr)

seed = seed_from_passphrase("my_passphrase")
scrambled = permute_pixels(raw, seed)
scrambled_image = bytes_to_image(scrambled, shape)
save_grayscale(scrambled_image, "test_data/baboon_PERMUTED.png")
print("Saved test_data/baboon_PERMUTED.png")

# verify it reverses correctly
restored = unpermute_pixels(scrambled, seed)
restored_image = bytes_to_image(restored, shape)
assert np.array_equal(arr, restored_image), "Permutation round-trip failed!"
print("Permutation round-trip OK.")