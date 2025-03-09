# zypper in python311-opencv-devel python311-numpy-devel python311-scikit-image
import cv2
import skimage.measure
import sys


def main():
    image = cv2.imread(sys.argv[1])
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    show_image_with_entropy(gray_image)

    # 1 splits, 2 parts of length 256, 25 iterations
    key = ([256, 256], 5)

    encrypted_image = encrypt_image(key, gray_image)
    show_image_with_entropy(encrypted_image)

    decrypted_image = decrypt_image(key, encrypted_image)
    show_image_with_entropy(decrypted_image)


def demo():
    image = cv2.imread(sys.argv[1])
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    show_image_with_entropy(gray_image)

    # 1 splits, 2 parts of length 256, 25 iterations
    key = ([256, 256], 5)

    i = 0
    encrypted_image = gray_image.copy()
    while True:
        encrypted_image = encrypt_image_bakers_map(encrypted_image, key[0])
        i += 1
        print(f"{i}th iteration")
        show_image_with_entropy(encrypted_image)


def encrypt_image(key: [list, int], image):
    n, iterations = key
    encrypted_image = image.copy()

    for i in range(iterations):
        encrypted_image = encrypt_image_bakers_map(encrypted_image, n)

    return encrypted_image


def encrypt_image_bakers_map(image, n: list):
    N, _ = image.shape
    encrypted_img = image.copy()

    for x in range(N):
        for y in range(N):
            _map_pixel(image, encrypted_img, (x, y), n)

    return encrypted_img


def _map_pixel(src_image, target_img, pixel_coords: tuple[int, int], n: list):
    N, _ = src_image.shape
    r, s = pixel_coords

    N_i = 0  # N_0 == 0
    for i in range(len(n)):
        if N_i <= r and r < N_i + n[i]:
            q_i = N // n[i]
            mapped_r = q_i * (r - N_i) + (s % q_i)
            mapped_s = ((s - (s % q_i)) // q_i) + N_i
            pixel = src_image[mapped_r][mapped_s]
            # target_img[r][s] = substitute(pixel, r, s)
            target_img[r][s] = pixel
            return

        N_i += n[i]  # N_i = n_1 + ... + n_i


def decrypt_image(key: [list, int], image):
    n, iterations = key
    decrypted_image = image.copy()

    for i in range(iterations):
        decrypted_image = decrypt_image_bakers_map(decrypted_image, n)

    return decrypted_image


def decrypt_image_bakers_map(image, n: list):
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
            # target_img[mapped_r][mapped_s] = unsubstitute(pixel, r, s)
            target_img[mapped_r][mapped_s] = pixel
            return

        N_i += n[i]  # N_i = n_1 + ... + n_i_image, (x, y), n)


def substitute(pixel, x, y):
    return (int(pixel) + x * y) % 256


def unsubstitute(pixel, x, y):
    return (int(pixel) - x * y) % 256


def _old_encrypt_image(image):
    length, _ = image.shape
    encrypted_img = image.copy()

    for x in range(length):
        for y in range(length):
            if x < length / 2:
                pixel = image[2 * x + y % 2][y // 2]
            else:
                pixel = image[2 * x - length + y % 2][(y + length) // 2]

            pixel = substitute(pixel, x, y)
            encrypted_img[x][y] = pixel

    return encrypted_img


def _old_decrypt_image(image):
    length, _ = image.shape
    decrypted_img = image.copy()

    for x in range(length):
        for y in range(length):
            if x < length / 2:
                mapped_x, mapped_y = 2 * x + y % 2, y // 2
            else:
                mapped_x, mapped_y = 2 * x - length + y % 2, (y + length) // 2

            pixel = unsubstitute(image[x][y], x, y)
            decrypted_img[mapped_x][mapped_y] = pixel

    return decrypted_img


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


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("need args")
        exit()
    else:
        demo()
