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

    print(measure_entropy(gray_image))


def measure_entropy(image):
    return skimage.measure.shannon_entropy(image)


if __name__ == "__main__":
    main()
