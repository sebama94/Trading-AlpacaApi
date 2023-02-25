from keras.optimizers import Adam

class ModelTrainer:
    def __init__(self, model, x_train, y_train, x_test, y_test):
        self.model = model
        self.x_train = x_train
        self.y_train = y_train
        self.x_test = x_test
        self.y_test = y_test

    def train_model(self, epochs, batch_size):
        self.model.compile(loss='mse', optimizer=Adam(lr=0.001))
        self.model.fit(self.x_train, self.y_train, epochs=epochs, batch_size=batch_size, validation_data=(self.x_test, self.y_test))
