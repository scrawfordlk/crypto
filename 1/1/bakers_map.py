# zypper in python311-opencv-devel python311-numpy-devel python311-scikit-image
import cv2
import skimage.measure


def main():
    image = cv2.imread("flower.jpg")
    cv2.imshow("Baker's Map Encryption", image)
    cv2.waitKey(0)

    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    cv2.imshow("Baker's Map Encryption", gray_image)
    cv2.waitKey(0)

    print_entropy(gray_image)

    encrypted_image = gray_image.copy()
    while True:
        encrypted_image = encrypt_image(encrypted_image)
        print_entropy(encrypted_image)
        cv2.imshow("Baker's Map Encryption", encrypted_image)
        key = cv2.waitKey(0)
        if key == ord("n"):
            continue
        elif key == ord("q"):
            cv2.destroyAllWindows()
            exit()


def encrypt_image(image):
    length, _ = image.shape
    encrypted_img = image.copy()

    for x in range(length):
        for y in range(length):
            if x < length / 2:
                encrypted_img[x][y] = image[2 * x + y % 2][y // 2]
            else:
                encrypted_img[x][y] = image[2 * x - length + y % 2][(y + length) // 2]

    return encrypted_img


def print_entropy(image):
    return print("Entropy: " + str(skimage.measure.shannon_entropy(image)))


if __name__ == "__main__":
    main()
