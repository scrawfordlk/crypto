# zypper in python311-opencv python311-numpy
import cv2, numpy, time
import skimage.measure


def main():
    image = cv2.imread("forest.jpg")
    cv2.imshow("Title of image", image)
    cv2.waitKey(0)

    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    cv2.imshow("Title of image", gray_image)
    key = cv2.waitKey(0)
    if key == ord("q"):
        cv2.destroyAllWindows()

    print("Entropy of initial image: " + measure_entropy(gray_image))
    encrypted_image = encrypt_image(gray_image)
    cv2.imshow("Encrypted image", encrypted_image)
    print("New entropy: " + measure_entropy(encrypt_image(image)))


def encrypt_image(image, iterations=1):
    height, width = image.shape()
    encrypted_image = image.copy()

    for _ in range(iterations):
        current_image = image.copy()
        for y in range(height):
            for x in range(width):
                if x < width / 2:
                    current_image[2 * x][y // 2] = image[x][y]
                else:
                    current_image[2 * x - 1][(y + 1) // 2] = image[x][y]
        encrypted_image = current_image
    return encrypted_image


def measure_entropy(image):
    return skimage.measure.shannon_entropy(image)


if __name__ == "__main__":
    main()
