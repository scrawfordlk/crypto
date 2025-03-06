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

    print("Entropy of initial image: " + str(measure_entropy(gray_image)))

    i = 1
    while True:
        encrypted_image = encrypt_image(gray_image, i)
        print("New entropy: " + str(measure_entropy(encrypted_image)))
        cv2.imshow("Baker's Map Encryption", encrypted_image)
        key = cv2.waitKey(0)
        if key == ord("n"):
            i += 1
            continue
        elif key == ord("q"):
            cv2.destroyAllWindows()
            exit()


def encrypt_image(image, iterations=1):
    length, _ = image.shape
    encrypted_image = image.copy()

    for i in range(iterations):
        temp_img = encrypted_image.copy()

        for x in range(length):
            for y in range(length):
                if x < length / 2:
                    temp_img[x][y] = encrypted_image[2 * x][y // 2]
                else:
                    temp_img[x][y] = encrypted_image[2 * x - length][(y + length) // 2]
        encrypted_image = temp_img

    return encrypted_image


def measure_entropy(image):
    return skimage.measure.shannon_entropy(image)


if __name__ == "__main__":
    main()
