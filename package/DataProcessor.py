import numpy as np

class DataProcessor:
    def __init__(self, data):
        self.data = data

    def split_data(self, split_ratio=0.8):
        split_index = int(len(self.data) * split_ratio)
        train_data = self.data[:split_index]
        test_data = self.data[split_index:]
        return train_data, test_data
