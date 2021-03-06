# -*- coding: utf-8 -*-  
import numpy as np
np.random.seed(1337)
from keras.models import Sequential, model_from_json
from keras.layers.core import Dense, Dropout, Activation
from keras.optimizers import SGD, Adam, RMSprop
from keras.utils import np_utils
from time import sleep

batch_size = 128
nb_classes = 20
nb_epoch = 1000
def load_data():
   x_train=[]
   Y_train=[]
   x_test=[]
   Y_test=[]
   
   f = open("distinguishsexdata/train.txt","r")
   i = 0
   for line in f.readlines():
       line = line.strip("\n").split(",")
       if i>0:
         Y_train.append(int(float(line[2])/5))
         del line[0]
         del line[0]
         del line[0]
         x_train.append(line)
       i += 1
   x1=np.array(x_train)
   y1=np.array(Y_train)
   f.close()
   
   f = open("distinguishsexdata/test.txt","r")
   i = 0
   for line in f.readlines():
       line = line.strip("\n").split(",")
       if i>0:
         Y_test.append(int(float(line[2])/5))
         del line[0]
         del line[0]
         del line[0]
         x_test.append(line)
       i += 1
   x2=np.array(x_test)
   y2=np.array(Y_test)
   f.close()

   return (x1, y1), (x2, y2)

(X_train, y_train), (X_test, y_test) = load_data()
X_train = X_train.reshape(1858, 26)
X_test = X_test.reshape(200, 26)
X_train = X_train.astype('float32')
X_test = X_test.astype('float32')
X_train /= 255
X_test /= 255
print(X_train.shape[0], 'train samples')
print(X_test.shape[0], 'test samples')
# binary class matrices
Y_train = np_utils.to_categorical(y_train, nb_classes)
Y_test = np_utils.to_categorical(y_test, nb_classes)

model = Sequential()
model.add(Dense(32, input_shape=(26,)))
model.add(Activation('relu'))
model.add(Dropout(0.2))
model.add(Dense(output_dim=32))
model.add(Activation('relu'))
model.add(Dropout(0.2))
model.add(Dense(output_dim=20))
model.add(Activation('softmax'))

sgd = SGD(lr=0.05, decay=1e-6, momentum=0.9, nesterov=True)
#model.compile(loss='categorical_crossentropy',optimizer=RMSprop(),metrics=['accuracy'])
model.compile(loss='categorical_crossentropy',optimizer=sgd,metrics=['accuracy'])
history = model.fit(X_train, Y_train,batch_size=batch_size, 
                    nb_epoch=nb_epoch,verbose=1, 
                    validation_data=(X_test, Y_test))
#??????????????????
# result = []
# result = model.predict_classes(X_test,batch_size=batch_size,verbose=1)
# for r in result:
#     print r

score = model.evaluate(X_test, Y_test, verbose=1)
print('loss:', score[0])
print('accuracy:', score[1])
print "end"

# #????????????
# json_string = model.to_json()
# open("model/model_json.json","w").write(json_string)
# #??????????????????????????????????????????
# model.save_weights("model/model_json_weight.h5")
# #?????????????????????
# model = model_from_json(open("model/model_json.json").read())
# model.load_weights("model/model_json_weight.h5")







