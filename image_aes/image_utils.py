import numpy as np
from PIL import Image

def load_grayscale(path: str) -> np.ndarray:
    img = Image.open(path).convert("L")   # 'L' = 8-bit grayscale
    return np.array(img, dtype=np.uint8)

def save_grayscale(arr: np.ndarray, path: str):
    Image.fromarray(arr.astype(np.uint8), mode="L").save(path)

def image_to_bytes(arr: np.ndarray) -> tuple[bytes, tuple]:
    return arr.tobytes(), arr.shape

def bytes_to_image(data: bytes, shape: tuple) -> np.ndarray:
    return np.frombuffer(data, dtype=np.uint8).reshape(shape)

if __name__ == "__main__":
    arr = load_grayscale("test_data/baboon.png")
    print("Loaded shape:", arr.shape, "dtype:", arr.dtype)

    raw_bytes, shape = image_to_bytes(arr)
    reconstructed = bytes_to_image(raw_bytes, shape)

    assert np.array_equal(arr, reconstructed), "Round-trip failed!"
    save_grayscale(reconstructed, "test_data/baboon_roundtrip_check.png")
    print("Image I/O round-trip OK.")