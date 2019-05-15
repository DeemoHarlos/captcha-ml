
from PIL import Image, ImageDraw, ImageFont
import numpy as np
from keras.models import Sequential
from keras.models import load_model
from keras.models import Model
from keras.layers import Input, Dense, Dropout, Flatten, Conv2D, MaxPooling2D
from keras.layers.normalization import BatchNormalization
from keras.utils  import np_utils
from keras.callbacks import ModelCheckpoint, EarlyStopping, TensorBoard
from keras import optimizers
import csv

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

def trans_image(image):
    a = np.array(image.convert("L"))
    b = np.array([np.array([[(1 if (x - 193>0) else 0)] for x in y]) for y in a])
    return b


#creat CNN model
print('Creating CNN model...')
tensor_in = Input((100, 120, 1))
tensor_out = tensor_in
tensor_out = Conv2D(filters=32, kernel_size=(3, 3), padding='same', activation='relu')(tensor_out)
tensor_out = Conv2D(filters=32, kernel_size=(3, 3), activation='relu')(tensor_out)
tensor_out = MaxPooling2D(pool_size=(2, 2))(tensor_out)
tensor_out = Conv2D(filters=64, kernel_size=(3, 3), padding='same', activation='relu')(tensor_out)
tensor_out = Conv2D(filters=64, kernel_size=(3, 3), activation='relu')(tensor_out)
tensor_out = MaxPooling2D(pool_size=(2, 2))(tensor_out)
tensor_out = Conv2D(filters=128, kernel_size=(3, 3), padding='same', activation='relu')(tensor_out)
tensor_out = Conv2D(filters=128, kernel_size=(3, 3), activation='relu')(tensor_out)
tensor_out = BatchNormalization(axis=1)(tensor_out)
tensor_out = MaxPooling2D(pool_size=(2, 2))(tensor_out)
tensor_out = Conv2D(filters=256, kernel_size=(3, 3), padding='same', activation='relu')(tensor_out)
tensor_out = Conv2D(filters=256, kernel_size=(3, 3), padding='same', activation='relu')(tensor_out)
tensor_out = MaxPooling2D(pool_size=(2, 2))(tensor_out)
tensor_out = Conv2D(filters=512, kernel_size=(3, 3), padding='same', activation='relu')(tensor_out)
tensor_out = BatchNormalization(axis=1)(tensor_out)
tensor_out = MaxPooling2D(pool_size=(2, 2))(tensor_out)

tensor_out = Flatten()(tensor_out)
tensor_out = Dropout(0.5)(tensor_out)

tensor_out = [Dense(26, name='digit1', activation='softmax')(tensor_out),\
              Dense(26, name='digit2', activation='softmax')(tensor_out),\
              Dense(26, name='digit3', activation='softmax')(tensor_out),\
              Dense(26, name='digit4', activation='softmax')(tensor_out)]

model = Model(inputs=tensor_in, outputs=tensor_out)
sgd = optimizers.SGD(lr=0.0001, decay=1e-6, momentum=0.9, nesterov=True)
model.compile(loss='categorical_crossentropy', optimizer=sgd, metrics=['accuracy'])
#model.compile(loss='categorical_crossentropy', optimizer='Adamax', metrics=['accuracy'])
model.summary()
              
print("Reading training data...")
#train_data = np.stack([np.array(Image.open("./test_img/" + str(index) + ".png"))/255.0 for index in range(0, 3000, 1)])
train_data = np.stack([trans_image(Image.open("./train_img_mixed/" + str(index) + ".png")) for index in range(0, 22500, 1)])
traincsv = open('./train_label_mixed.csv', 'r', encoding = 'utf8')
read_label =  [to_onelist(row[0]) for row in csv.reader(traincsv)]
train_label = [[] for _ in range(4)]
for arr in read_label:
    for index in range(4):
        train_label[index].append(arr[index])
train_label = [arr for arr in np.asarray(train_label)]
print("Shape of train data:", train_data.shape)

print("Reading validation data...")
#vali_data = np.stack([np.array(Image.open("./test_img/"+ str(index) + ".png"))/255.0 for index in range(0, 3000, 1)])
vali_data = np.stack([trans_image(Image.open("./valid_img_mixed/" + str(index) + ".png")) for index in range(0, 250, 1)])
valicsv = open('./valid_label_mixed.csv', 'r', encoding = 'utf8')
read_label = [to_onelist(row[0]) for row in csv.reader(valicsv)]
vali_label = [[] for _ in range(4)]
for arr in read_label:
    for index in range(4):
        vali_label[index].append(arr[index])
vali_label = [arr for arr in np.asarray(vali_label)]
print("Shape of train data:", vali_data.shape)


filepath='./cnn_model.hdf5'
#try:
#    model = load_model(filepath)
#    print('model is loaded...')
#except:
model.save(filepath)
print('training new model...')

checkpoint = ModelCheckpoint(filepath, monitor='val_digit4_acc', verbose=1, save_best_only=True, mode='max')
earlystop = EarlyStopping(monitor='val_loss', patience=8, verbose=1, mode='auto')
tensorBoard = TensorBoard(log_dir = './logs', histogram_freq = 1)
callbacks_list = [tensorBoard, earlystop, checkpoint]
model.fit(train_data, train_label, batch_size=25, epochs=100, verbose=2, validation_data=(vali_data, vali_label), callbacks=callbacks_list)
#.fit(train_data, train_label, validation_split=0.2, batch_size=50, epochs=20, verbose=2, callbacks=callbacks_list)
# tensorboard --logdir= (dist)