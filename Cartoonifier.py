from random import randint
import argparse
import cv2 as cv
import numpy as np

ap = argparse.ArgumentParser(
    description="a simple program to create cartoonish camera effect",
    usage='python %(prog)s [-h] [-i PATH]')
ap.add_argument(
    "-i",
    "--input",
    default=None,
    metavar='PATH',
	help="create cartoon image from image in given path")
args = vars(ap.parse_args())

def cartoonify(img, mode):
    """
    Apply cartoon effect to the input image based on the selected mode.

    Parameters:
    img (numpy.ndarray): Input image to be cartoonified.
    mode (str): Mode of cartoonification. Possible values are:
                - '' (empty string): returns the original image.
                - 'edge': returns the image with edges highlighted.
                - 'reduceNoise': returns the image with reduced noise.
                - 'blackAndWhite': returns the image in black and white.
                - 'normal': returns the image with cartoon effect.

    Returns:
    numpy.ndarray: Cartoonified image based on the selected mode.
    """

    gray_img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    smooth_gray_img = cv.bilateralFilter(gray_img, 5, 75, 75)
    edge = cv.adaptiveThreshold(smooth_gray_img, 255,
                                cv.ADAPTIVE_THRESH_GAUSSIAN_C,
                                cv.THRESH_BINARY, 5, 1)
    color_img = cv.bilateralFilter(img, 9, 900, 900)

    if mode == 'edge':
        return cv.cvtColor(edge, cv.COLOR_GRAY2BGR)
    elif mode == 'reduceNoise':
        smooth_edge = cv.bilateralFilter(edge, 9, 150, 150)
        mask = cv.threshold(smooth_edge, 110, 255, cv.THRESH_BINARY) [1]
        return cv.bitwise_and(color_img, color_img, mask=mask)
    elif mode == 'blackAndWhite':
        return cv.cvtColor(cv.bitwise_and(smooth_gray_img, smooth_gray_img, mask=edge),
                           cv.COLOR_GRAY2BGR)
    elif mode == 'normal':
        return cv.bitwise_and(color_img, color_img, mask=edge)
    else:
        return img

def add_text(img, text):
    """
    Adds text to an image using a bitwise XOR operation.
    
    Args:
    img (numpy.ndarray): The image to add text to.
    text (numpy.ndarray): The text to add to the image.
    
    Returns:
    numpy.ndarray: The resulting image with the added text.
    """
    return cv.bitwise_xor(img, text)

def create_text(img):
    """
    Creates a text image with instructions for the user to interact with the cartoonifier program.

    Parameters:
    img (numpy.ndarray): The input image to be processed.

    Returns:
    numpy.ndarray: A text image with instructions to interact with the cartoonifier program.
    """

    width, height, depth = img.shape
    text = np.array([[[0]*depth]*height]*width, dtype='uint8')

    cv.putText(text, 'n for normal cartoon', (10, 20),
               cv.FONT_HERSHEY_COMPLEX_SMALL, 0.75, (255, 255, 255))
    cv.putText(text, 'b for black and white cartoon', (10, 40),
               cv.FONT_HERSHEY_COMPLEX_SMALL, 0.75, (255, 255, 255))
    cv.putText(text, 'e for edge cartoon', (10, 60),
               cv.FONT_HERSHEY_COMPLEX_SMALL, 0.75, (255, 255, 255))
    cv.putText(text, 'r for noise reduction', (10, 80),
               cv.FONT_HERSHEY_COMPLEX_SMALL, 0.75, (255, 255, 255))
    cv.putText(text, 'o for original image', (10, 100),
               cv.FONT_HERSHEY_COMPLEX_SMALL, 0.75, (255, 255, 255))
    cv.putText(text, 's to save image', (10, 120),
               cv.FONT_HERSHEY_COMPLEX_SMALL, 0.75, (255, 255, 255))
    cv.putText(text, 'q to quit', (10, 140),
               cv.FONT_HERSHEY_COMPLEX_SMALL, 0.75, (255, 255, 255))
    return text

def main():
    """
    The main function of the program.
    """
    is_using_cam = True
    cam = cv.VideoCapture(0)

    if args["input"] is not None:
        is_using_cam = False

        print("[I] read image in path")
        img = cv.imread(args["input"])

        if img is None:
            print("(E) cannot read image from the given path, check if the path is an image or not")
            raise SystemExit(0)

        n = img.shape[0]/480
        img = cv.resize(img,
                        tuple(int(x//n) for x in img.shape[1::-1]),
                        interpolation=cv.INTER_AREA)

    else:
        print("[I] opening camera")
        success, img = cam.read()

        if not success:
            print("(E) cannot read image from camera or camera not found, \
                  check if the camera is connected correctly")
            raise SystemExit(0)

    text = create_text(img)
    mode = 'normal'

    print("[I] applying cartoon effect")
    while True:
        if is_using_cam:
            img = cam.read() [1]

        cv.imshow('Cartoon Camera', add_text(cartoonify(img, mode), text))

        key = cv.waitKey(1)
        if key == ord('b'):
            mode = 'blackAndWhite'
        elif key == ord('n'):
            mode = 'normal'
        elif key == ord('r'):
            mode = 'reduceNoise'
        elif key == ord('e'):
            mode = 'edge'
        elif key == ord('o'):
            mode = ''
        elif key == ord('s'):
            name = mode+"_IMG_"+str(randint(1000,9999))+".jpg"
            cv.imwrite(name, cartoonify(img, mode))
        elif key == ord('q'):
            break

    cv.destroyAllWindows()
    cam.release()

if __name__ == "__main__":
    main()
    