"""
A simple script that tracks objects based on the color selected with the left mouse button.
"""
import cv2
import numpy as np
import argparse

hsv_image = None
low = None
high = None
color = None


def mouse_handler(event, x, y, flags, param):
    global color, low, high, hsv_image

    if event == cv2.EVENT_LBUTTONDOWN:
        hue = hsv_image[y, x, 0]
        saturation = hsv_image[y, x, 1]
        value = hsv_image[y, x, 2]

        color = np.array([hue, saturation, value])
        low = np.array([hue - 10, saturation - 70, value - 80])
        high = np.array([hue + 10, saturation + 70, value + 80])


def main(args):
    global color, low, high, hsv_image
    is_paused = False

    kernel = np.ones((5, 5), np.uint8)
    window_name = 'Video'
    cv2.namedWindow(window_name)
    cv2.setMouseCallback(window_name, mouse_handler)

    video = cv2.VideoCapture(args.input if args.input is not None else 0)
    captured, frame = video.read()

    RED = [0, 0, 255]  # bgr

    while captured:
        hsv_image = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        if color is not None:
            mask = cv2.inRange(hsv_image, low, high)
            mask = cv2.erode(mask, kernel, iterations=2)
            mask = cv2.dilate(mask, kernel, iterations=5)

            cnts = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            cnts = cnts[0] if len(cnts) == 2 else cnts[1]

            for c in cnts:
                x, y, w, h = cv2.boundingRect(c)
                cv2.rectangle(frame, (x, y), (x + w, y + h), RED, 2)

        cv2.imshow(window_name, frame)
        key = cv2.waitKey(1)

        if key == ord('q'):
            break
        if key == ord('p'):
            is_paused = not is_paused

        if not is_paused:
            captured, frame = video.read()


def parse_arguments():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('-i', '--input', required=False, default=None,
                        help='path to video that we will work with')
    return parser.parse_args()


if __name__ == '__main__':
    main(parse_arguments())
