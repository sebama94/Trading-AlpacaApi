from keras.models import Sequential
from keras.layers import Dense

class ModelSelector:
    def __init__(self, X_train):
        self.model = Sequential()
        self.model.add(Dense(64, input_shape=(X_train.shape[1],), activation='relu'))
        self.model.add(Dense(64, activation='relu'))
        self.model.add(Dense(1, activation='linear'))

