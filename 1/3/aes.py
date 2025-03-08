# zypper in python311-pycryptodome
import cv2
import skimage.measure
from Crypto.Cipher import AES
import sys


def main():
    image = cv2.imread(sys.argv[1])
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # show_image_with_entropy(image)
    entropy = measure_entropy(image)
    store_image("gray_" + str(entropy) + "_" + sys.argv[1], image)

    cipher_key = b"my 16 byte key!!"
    nonces, encrypted_image = encrypt_image(cipher_key, image)
    # show_image_with_entropy(encrypted_image)
    entropy = measure_entropy(encrypted_image)
    store_image("encrypted_" + str(entropy) + "_" + sys.argv[1], encrypted_image)

    # decrypted_image = decrypt_image(nonces, cipher_key, encrypted_image)
    # show_image_with_entropy(decrypted_image)


def encrypt_image(key, image):
    width, height = image.shape
    flat_original = image.flatten()
    flat_encrypted = flat_original.copy()
    nonces = []

    for i in range(0, len(flat_original), 16):
        cipher = AES.new(key, AES.MODE_EAX)
        nonces.append(cipher.nonce)
        pixels = flat_original[i : i + 16]

        encrypted_bytes = cipher.encrypt(b"".join(pixels))
        for j in range(16):
            flat_encrypted[i + j] = encrypted_bytes[j]

    encrypted_image = flat_encrypted.reshape((width, height))
    return nonces, encrypted_image


def decrypt_image(nonces, key, image):
    width, height = image.shape
    flat_encrypted = image.flatten()
    flat_decrypted = flat_encrypted.copy()

    for i in range(0, len(flat_encrypted), 16):
        cipher = AES.new(key, AES.MODE_EAX, nonce=nonces[i // 16])
        pixels = flat_encrypted[i : i + 16]

        decrypted_bytes = cipher.decrypt(b"".join(pixels))
        for j in range(16):
            flat_decrypted[i + j] = decrypted_bytes[j]

    return flat_decrypted.reshape((width, height))


def measure_entropy(image):
    return skimage.measure.shannon_entropy(image)


def print_entropy(image):
    return print("Entropy: " + str(measure_entropy(image)))


def show_image_with_entropy(image):
    print_entropy(image)
    cv2.imshow("Image", image)
    key = cv2.waitKey(0)
    if key == ord("q"):
        cv2.destroyAllWindows()
        exit()
    elif key == ord("n"):
        return


def store_image(file_name, image):
    cv2.imwrite(file_name, image)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("<program> <image>")
        exit()
    else:
        main()
