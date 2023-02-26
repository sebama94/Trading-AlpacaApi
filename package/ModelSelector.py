from keras.models import Sequential
from keras.layers import Dense

class ModelSelector:
    def __init__(self, input_shape):
        self.model = Sequential()
        self.model.add(Dense(32, input_shape=(input_shape,), activation='relu'))
        self.model.add(Dense(32, activation='relu'))
        self.model.add(Dense(units=32, activation='sigmoid'))
        self.model.add(Dense(32, activation='softmax'))
