from keras.optimizers import Adam
from keras.utils import plot_model
import matplotlib.pyplot as pyplot
from keras.utils import custom_object_scope

class ModelTrainer:
    def __init__(self, model, x_train, y_train, x_test, y_test):
        self.model = model

        print("sono dentolo la funznone ", model)
        self.x_train = x_train
        self.y_train = y_train
        self.x_test = x_test
        self.y_test = y_test
        self.history = None

    def train_model(self, epochs, batch_size):
        #self.model.compile(loss='mse', optimizer=Adam(lr=0.001), run_eagerly=True)
        self.model.compile(loss='mean_squared_error', metrics=['accuracy'], optimizer='adam', run_eagerly=True)
        print()
        self.history = self.model.fit(self.x_train, self.y_train, epochs=epochs, batch_size=batch_size, validation_data=(self.x_test, self.y_test))

    def plot(self):

        pyplot.title('model accuracy')
        # pyplot.legend(['train', 'test'], loc='upper left')
        # pyplot.show()
        # summarize history for loss
        # pyplot.plot(self.history.history['loss'])
        # pyplot.plot(self.history.history['val_loss'])
        # pyplot.title('model loss')
        pyplot.ylabel('accuracy')
        pyplot.xlabel('epoch')
        pyplot.legend(['train', 'test'], loc='upper left')
        # pyplot.show()
        pyplot.grid()

        print(self.history.history['accuracy'])
        print(self.history.history['val_accuracy'])
        pyplot.plot(self.history.history['accuracy'])
        pyplot.plot(self.history.history['val_accuracy'])

        # pyplot.plot(self.history)
        # pyplot.plot(self.history.history['mean_absolute_error'])
        # pyplot.plot(self.history.history['mean_absolute_percentage_error'])
        # pyplot.plot(self.history.history['cosine_proximity'])

        pyplot.show()