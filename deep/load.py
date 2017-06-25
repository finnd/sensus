from keras.models import Sequential
from keras.layers import Dense
import numpy

numpy.random.seed(7)

#load dataset

dataset = numpy.loadtxt("../acquisition/test_output.csv", delimiter=",")

#define input and output array

input_values = dataset[:,0:8]
output_values = dataset[:,8]

#create model

model = Sequential()
model.add(Dense(12, input_dim=8, activation='relu'))
model.add(Dense(8, activation='relu'))
model.add(Dense(1, activation='sigmoid'))

#compile model
model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

#Fit the model

model.fit(X, T, epocs=150, batch_size=10)

#Evaluate

scores = model.evaluate(X, Y)
print("\n%s: %.2f%%" % (model.metrics_names[1], scores[1]*100))