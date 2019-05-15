from PIL import Image, ImageDraw, ImageFont
import sys
import numpy as np

#np.set_printoptions(threshold=sys.maxsize)

def trans_image(image):
    a = np.array(image.convert("L"))
    b = np.array([np.array([(1 if (x - 193>0) else 0) for x in y]) for y in a])
    return b

train_data = np.stack([trans_image(Image.open("./test_img/" + str(index) + ".png")) for index in range(0, 3, 1)])

print(train_data)