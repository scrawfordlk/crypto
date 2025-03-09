# zypper in python311-opencv-devel python311-numpy-devel python311-scikit-image
import cv2
import skimage.measure
import sys


def main():
    image = cv2.imread(sys.argv[1])
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    show_image_with_entropy(gray_image)

    key = b"Tis a 16byte key"

    encrypted_image = gray_image.copy()
    while True:
        # encrypted_image = encrypt_image(encrypted_image)
        encrypted_image, n = encrypt_image_bakers_map(key, encrypted_image)
        show_image_with_entropy(encrypted_image)
        decrypted_image, n = decrypt_image_bakers_map(key, encrypted_image)
        print("DECRYPT")
        show_image_with_entropy(decrypted_image)


def encrypt_image_bakers_map(key, image):
    N, _ = image.shape
    encrypted_img = image.copy()
    n = get_n(image)

    for x in range(N):
        for y in range(N):
            _map_pixel(image, encrypted_img, (x, y), n)

    return encrypted_img, n


def _map_pixel(src_image, target_img, pixel_coords: tuple[int, int], n: list):
    N, _ = src_image.shape
    r, s = pixel_coords

    N_i = 0  # N_0 == 0
    for i in range(len(n)):
        if N_i <= r and r < N_i + n[i]:
            q_i = N // n[i]
            mapped_x = q_i * (r - N_i) + (s % q_i)
            mapped_y = ((s - (s % q_i)) // q_i) + N_i
            target_img[r][s] = src_image[mapped_x][mapped_y]
            return

        N_i += n[i]  # N_i = n_1 + ... + n_i


def decrypt_image_bakers_map(key, image):
    N, _ = image.shape
    decrypted_image = image.copy()
    n = get_n(image)

    for x in range(N):
        for y in range(N):
            _map_pixel(image, decrypted_image, (x, y), n)

    return decrypted_image, n


def _unmap_pixel(src_image, target_img, pixel_coords: tuple[int, int], n: list):
    N, _ = src_image.shape
    r, s = pixel_coords

    N_i = 0  # N_0 == 0
    for i in range(len(n)):
        if N_i <= r and r < N_i + n[i]:
            q_i = N // n[i]
            mapped_x = q_i * (r - N_i) + (s % q_i)
            mapped_y = ((s - (s % q_i)) // q_i) + N_i
            target_img[r][s] = src_image[mapped_x][mapped_y]
            return

        N_i += n[i]  # N_i = n_1 + ... + n_i


# per Definition of N, n_i and N_i
def get_n(image):
    # N, _ = image.shape
    # N_i = 0
    # n = []
    #
    # while N_i < N:
    #     n_i = 2 ** random.randint(1, 9)  # divides a 512x512 image
    #     if N_i + n_i > N and N % n_i == 0:
    #         n_i = N - N_i  #  assign rest
    #     N_i += n_i
    #     n.append(n_i)
    #
    # print(f"The n's are: {n}")
    return [256, 256]  # need to be sorted?


def encrypt_image(image):
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


def decrypt_image(image):
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


if __name__ == "__main__":
    if len(sys.argv) != 2:
        exit()
    else:
        main()
