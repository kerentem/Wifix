import numpy as np
import tensorflow as tf
from tensorflow.keras.layers import LSTM, Dense
from sklearn.metrics import mean_absolute_error

from .pricing_data import wifi_data


class DynamicPricing:
    def __init__(self):
        self.data = wifi_data
        self.model = None
        self.train_model()
        self.evaluate_model()

    def train_model(self):
        num_features = len(self.data[0]["input"])
        X = [entry["input"] for entry in self.data]
        y = [entry["demand"] for entry in self.data]

        model = tf.keras.Sequential(
            [LSTM(units=64, input_shape=(None, num_features)), Dense(units=1)]
        )
        model.compile(optimizer="adam", loss="mean_squared_error")

        X = np.array(X)
        y = np.array(y)
        model.fit(X, y, epochs=100, batch_size=32)

        self.model = model

    def evaluate_model(self):
        test_size = int(len(self.data) * 0.2)
        test_data = self.data[-test_size:]

        X_test = np.array([entry["input"] for entry in test_data])
        y_test = np.array([entry["demand"] for entry in test_data])

        y_pred = self.model.predict(X_test).flatten()
        mae = mean_absolute_error(y_test, y_pred)
        print(f"Mean Absolute Error: {mae:.2f}")

    def calculate_predicted_demand(self, input_features):
        predicted_demand = self.model.predict(np.array([input_features]))[0][0]
        return predicted_demand

    def calculate_price(self, payment_method, input_features) -> float:
        predicted_demand = self.calculate_predicted_demand(input_features)

        base_price = 0.10
        user_factor = 0.05
        demand_factor = predicted_demand * user_factor

        if payment_method == "basic":
            price = base_price + demand_factor
        elif payment_method == "premium":
            price = base_price + demand_factor * 1.5
        elif payment_method == "business":
            price = base_price + demand_factor * 2.0
        else:
            raise ValueError("Invalid payment method")

        return price
