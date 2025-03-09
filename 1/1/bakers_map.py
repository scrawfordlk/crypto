# zypper in python311-opencv-devel python311-numpy-devel python311-scikit-image
import cv2
import skimage.measure
import sys
import time
import matplotlib.pyplot as plt


def encrypt_image(key: [list, int], image):
    n, iterations = key
    encrypted_image = image.copy()

    for i in range(iterations):
        encrypted_image = _encrypt_image_bakers_map(encrypted_image, n)

    return encrypted_image


def _encrypt_image_bakers_map(image, n: list):
    N, _ = image.shape
    encrypted_img = image.copy()

    for x in range(N):
        for y in range(N):
            _map_pixel(image, encrypted_img, (x, y), n)

    return encrypted_img


def _map_pixel(src_image, target_img, pixel_coords: tuple[int, int], n: list):
    N, _ = src_image.shape
    r, s = pixel_coords

    N_i = 0  # N_0 = 0
    for i in range(len(n)):
        if N_i <= r and r < N_i + n[i]:
            q_i = N // n[i]
            mapped_r = q_i * (r - N_i) + (s % q_i)
            mapped_s = ((s - (s % q_i)) // q_i) + N_i
            pixel = src_image[mapped_r][mapped_s]
            target_img[r][s] = substitute(pixel, r, s)
            return

        N_i += n[i]  # N_i = n_1 + ... + n_i


def decrypt_image(key: [list, int], image):
    n, iterations = key
    decrypted_image = image.copy()

    for i in range(iterations):
        decrypted_image = _decrypt_image_bakers_map(decrypted_image, n)

    return decrypted_image


def _decrypt_image_bakers_map(image, n: list):
    N, _ = image.shape
    decrypted_image = image.copy()

    for x in range(N):
        for y in range(N):
            _unmap_pixel(image, decrypted_image, (x, y), n)

    return decrypted_image


def _unmap_pixel(src_image, target_img, pixel_coords: tuple[int, int], n: list):
    N, _ = src_image.shape
    r, s = pixel_coords

    N_i = 0  # N_0 == 0
    for i in range(len(n)):
        if N_i <= r and r < N_i + n[i]:
            q_i = N // n[i]
            mapped_r = q_i * (r - N_i) + (s % q_i)
            mapped_s = ((s - (s % q_i)) // q_i) + N_i
            pixel = src_image[r][s]
            target_img[mapped_r][mapped_s] = unsubstitute(pixel, r, s)
            return

        N_i += n[i]  # N_i = n_1 + ... + n_i_image, (x, y), n)


def substitute(pixel, x, y):
    return (int(pixel) + x * y) % 256


def unsubstitute(pixel, x, y):
    return (int(pixel) - x * y) % 256


def show_image_with_entropy(image):
    print_entropy(image)
    cv2.imshow("Image", image)
    key = cv2.waitKey(0)
    if key == ord("q"):
        cv2.destroyAllWindows()
        exit()
    elif key == ord("n"):
        return


def print_entropy(image):
    return print("Entropy: " + str(skimage.measure.shannon_entropy(image)))


def measure_entropy(image):
    return skimage.measure.shannon_entropy(image)


def store_image(file_name, image):
    cv2.imwrite(file_name, image)


def plot_results(iterations, entropies, file_name):
    plt.plot(iterations, entropies)
    plt.xlabel("Iterationen")
    plt.ylabel("Entropie")
    plt.savefig(file_name + ".pdf", format="pdf", bbox_inches="tight")
    plt.show()


def main():
    image = cv2.imread(sys.argv[2])
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    show_image_with_entropy(gray_image)

    # 1 splits, 2 parts of length 256, 25 iterations
    key = ([256, 256], 20)

    encrypted_image = encrypt_image(key, gray_image)
    show_image_with_entropy(encrypted_image)

    decrypted_image = decrypt_image(key, encrypted_image)
    show_image_with_entropy(decrypted_image)


def demo():
    image = cv2.imread(sys.argv[2])
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    show_image_with_entropy(gray_image)

    entropy = measure_entropy(gray_image)
    print(f"entropy: {entropy}")

    # 1 splits, 2 parts of length 256, 25 iterations
    key = ([256, 256], 5)

    i = 0
    encrypted_image = gray_image.copy()
    while True:
        i += 1
        encrypted_image = _encrypt_image_bakers_map(encrypted_image, key[0])
        print(f"{i}th iteration")
        show_image_with_entropy(encrypted_image)


def plot_demo():
    start = time.time()
    image = cv2.imread(sys.argv[2])
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    entropy = measure_entropy(gray_image)
    print(f"Entropy: {entropy}")

    # 1 splits, 2 parts of length 256, 25 iterations
    key = ([256, 256], 30)

    iterations = []
    entropies = []

    i = 0
    encrypted_image = gray_image.copy()
    while i < key[1]:
        encrypted_image = _encrypt_image_bakers_map(encrypted_image, key[0])
        i += 1
        iterations.append(i)
        end = time.time()
        entropy = measure_entropy(encrypted_image)
        entropies.append(entropy)
        print(f"{i}th iteration, time elapsed: {end - start}, entropy: {entropy}")
        # store_image(f"out/{i}_{entropy}_{sys.argv[2]}", encrypted_image)

    plot_results(iterations, entropies, "out/" + sys.argv[2][:-4])


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("<program> < main | demo | plot> <file_name>")
        exit()
    else:
        if sys.argv[1] == "main":
            main()
        elif sys.argv[1] == "plot":
            plot_demo()
        else:
            demo()
