import numpy as np
import matplotlib.pyplot as plt
import hashlib

def seed_from_passphrase(passphrase: str) -> float:
    # Deterministic seed in (0,1) from a passphrase, so same passphrase -> same sequence
    h = hashlib.sha256(passphrase.encode()).hexdigest()
    val = int(h, 16) / (16 ** len(h))
    return 0.0001 + val * 0.9998   # keep strictly inside (0,1), away from edges

def logistic_sequence(seed: float, length: int, r: float = 3.99) -> np.ndarray:
    """
    seed: initial value in (0, 1), exclusive
    r: control parameter; 3.57 to 4.0 gives chaotic behavior, 3.99 is safely deep in it
    """
    x = seed
    seq = np.empty(length)
    for i in range(length):
        x = r * x * (1 - x)
        seq[i] = x
    return seq

if __name__ == "__main__":
    seed = seed_from_passphrase("my_passphrase")
    seq = logistic_sequence(seed, 2000, r=3.99)

    # Reproducibility check — same seed must always give the same sequence
    seq2 = logistic_sequence(seed, 2000, r=3.99)
    assert np.array_equal(seq, seq2), "Not reproducible!"

    plt.plot(seq[:200])
    plt.title("Logistic map output (first 200 values)")
    plt.xlabel("n")
    plt.ylabel("x_n")
    plt.savefig("chaotic/logistic_sequence_plot.png")

    print("Seed:", seed)
    print("Sequence reproducible: OK")
    print("Saved plot to chaotic/logistic_sequence_plot.png")

def generate_permutation(seed: float, length: int, r: float = 3.99) -> np.ndarray:
    """
    Uses the chaotic sequence to generate a permutation (shuffled order)
    of indices 0..length-1. This same seed always produces the same
    permutation, which is what makes decryption possible.
    """
    seq = logistic_sequence(seed, length, r)
    # argsort gives the indices that would sort the sequence — 
    # since the sequence is chaotic, this ordering looks random
    permutation = np.argsort(seq)
    return permutation

def permute_pixels(pixel_bytes: bytes, seed: float) -> bytes:
    arr = np.frombuffer(pixel_bytes, dtype=np.uint8)
    perm = generate_permutation(seed, len(arr))
    scrambled = arr[perm]
    return scrambled.tobytes()

def unpermute_pixels(scrambled_bytes: bytes, seed: float) -> bytes:
    arr = np.frombuffer(scrambled_bytes, dtype=np.uint8)
    perm = generate_permutation(seed, len(arr))
    # to reverse: place each scrambled value back at its original index
    original = np.empty_like(arr)
    original[perm] = arr
    return original.tobytes()

def diffuse_pixels(pixel_bytes: bytes, seed: float, r: float = 3.99) -> bytes:
    arr = np.frombuffer(pixel_bytes, dtype=np.uint8).copy()
    seq = logistic_sequence(seed, len(arr), r)
    # Convert chaotic sequence to byte-range keystream
    keystream = (seq * 256).astype(np.uint8)

    diffused = np.empty_like(arr)
    prev = 0
    for i in range(len(arr)):
        diffused[i] = arr[i] ^ keystream[i] ^ prev
        prev = diffused[i]  # chain: each output depends on the previous output
    return diffused.tobytes()

def undiffuse_pixels(diffused_bytes: bytes, seed: float, r: float = 3.99) -> bytes:
    arr = np.frombuffer(diffused_bytes, dtype=np.uint8)
    seq = logistic_sequence(seed, len(arr), r)
    keystream = (seq * 256).astype(np.uint8)

    original = np.empty_like(arr)
    prev = 0
    for i in range(len(arr)):
        original[i] = arr[i] ^ keystream[i] ^ prev
        prev = arr[i]  # chain uses the diffused value, not the recovered original
    return original.tobytes()    