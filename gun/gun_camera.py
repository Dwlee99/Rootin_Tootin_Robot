from picamera import PiCamera
from time import sleep
from io import BytesIO
import cv2
from PIL import Image
import numpy as np

camera = PiCamera()
camera.exposure_mode = 'antishake'
camera.resolution = (height, width) = (1024, 768)
capture_time = 0.1
bullet_radius = 50
r = bullet_radius

def take_photo():
    image = np.empty((width, height, 3), dtype=np.uint8)
    camera.start_preview()
    sleep(capture_time)
    camera.capture(image, format="rgb")
    Image.fromarray(image.astype('uint8')).convert('RGB').save('big.jpg')
    x, y, _ = image.shape
    temp = image[x//2-r:x//2+r, y//2-r:y//2+r]
    Image.fromarray(temp.astype('uint8')).convert('RGB').save('small.jpg')
    camera.stop_preview()
    return cv2.cvtColor(image, cv2.COLOR_RGB2HSV)

# credit https://stackoverflow.com/a/72138638 for these color ranges and masking
hsv_ranges = [
    ['white', [0, 0, 168], [180, 111, 255]],
    ['red', [0, 160, 70], [10, 250, 250]],
    ['pink', [0, 50, 70], [10, 160, 250]],
    ['yellow', [15, 50, 70], [30, 250, 250]],
    ['green', [40, 50, 70], [70, 250, 250]],
    ['cyan', [80, 50, 70], [90, 250, 250]],
    ['blue', [100, 50, 70], [130, 250, 250]],
    ['purple', [140, 50, 70], [160, 250, 250]],
    ['red', [170, 160, 70], [180, 250, 250]],
    ['pink', [170, 50, 70], [180, 160, 250]],
    ['black', [0, 0, 0], [180, 255, 70]]
]

def color_in_center(image):
    x, y, _ = image.shape
    # cv2.imwrite("full.jpg", image)
    image = image[x//2-r:x//2+r, y//2-r:y//2+r]
    # cv2.imwrite("small.jpg", image)
    color_found = 'none'
    max_count = 0
    for name, low, high in hsv_ranges:
        mask = cv2.inRange(image, np.array(low), np.array(high))
        count = np.sum(mask)
        #print(name)
        #print(count)
        if count > max_count:
            color_found = name
            max_count = count
    return color_found

# image = take_photo()
# print(color_in_center(image))
