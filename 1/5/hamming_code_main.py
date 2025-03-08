import hamming
from bitarray import bitarray
import sys


def main():
    msg = bitarray(sys.argv[1])
    print(f"Original Bits: {msg}")
    print()

    encoded_msg = hamming.encode(msg)
    print(f"Encoded Bits: {encoded_msg}")

    decoded_msg = hamming.decode(encoded_msg)
    print(f"Decoded Bits: {decoded_msg}")
    print()

    # simulating corruption
    corrupt_encoded_msg = encoded_msg.copy()
    corrupt_encoded_msg[6] = corrupt_encoded_msg[6] ^ 1
    print(f"Corrupted encoded Bits: {corrupt_encoded_msg}")

    corrupt_decoded_msg = hamming.decode(corrupt_encoded_msg)
    print(f"Decoded Bits: {corrupt_decoded_msg}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        exit()
    else:
        main()
