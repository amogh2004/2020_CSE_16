import cv2
import numpy as np

canvas = np.ones((725, 725))*255
points = np.array(
    [
        [[4,4]],
        [[4,256]],
        [[256,256]],
        [[256,4]]
        
    ]
)

cv2.drawContours(canvas, [points], -1, (0,0,0), 2)
cv2.imshow('image', canvas)
cv2.waitKey(0)
