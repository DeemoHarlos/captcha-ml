from PIL import Image, ImageDraw, ImageFont
import numpy as np
from keras.models import Sequential
from keras.models import load_model
from keras.models import Model
from keras.layers import Input, Dense, Dropout, Flatten, Conv2D, MaxPooling2D
from keras.utils  import np_utils
from keras.callbacks import ModelCheckpoint, EarlyStopping, TensorBoard
import csv
import time

dic = {'a':0,'b':1,'c':2,'d':3,'e':4,'f':5,'g':6,'h':7,'i':8,'j':9,'k':10,'l':11,'m':12,'n':13,'o':14,'p':15,'q':16,'r':17,'s':18,'t':19,'u':20,'v':21,'w':22,'x':23,'y':24,'z':25}

def to_onelist(text):
    label_list = []
    for c in text:
        onehot = [0 for _ in range(26)]
        onehot[ dic[c] ] = 1
        label_list.append(onehot)
    return label_list

def to_text(l_list):
    text=[]
    pos = []
    for i in range(4):
        for j in range(26):
            if(l_list[i][j]):
                pos.append(j)

    for i in range(4):
        char_idx = pos[i]
        text.append(list(dic.keys())[list(dic.values()).index(char_idx)])
        return "".join(text)

def to_text2(int):
    text = []
    text.append(list(dic.keys())[list(dic.values()).index(int)])
    return "".join(text)

def trans_image(image):
    a = np.array(image.convert("L"))
    b = np.array([np.array([[(1 if (x - 193>0) else 0)] for x in y]) for y in a])
    return b

print('model loading...')
model = load_model('./cnn_model_FONT22500.hdf5')

print("Reading data...")
x_train = np.stack([trans_image(Image.open("./unlabeled_img_real/" + str(index) + ".png")) for index in range(3000, 20000 , 1)])

print('predict start')
tStart = time.time()#計時開始

prediction = model.predict(x_train)
print('predicted ')
resultlist = ["" for _ in range(17000)]

for predict in prediction:
    for index in range(17000):
        resultlist[index] += to_text2(np.argmax(predict[index]))

tEnd = time.time()#計時結束


predict_csv = open('./unlabeled_label_real.csv', 'w+', encoding = 'utf8')

for result in resultlist:
    predict_csv.write(result + '\n')

#列印計時結果
print ('It cost %f sec' % (tEnd - tStart)) #會自動做近位
predict_csv.close()