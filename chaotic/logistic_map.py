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
    