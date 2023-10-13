from pandas import DataFrame
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import LabelEncoder
from joblib import load, dump
from datetime import datetime
import os

# Define the project root path
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

class Machine:
    def __init__(self, df):
        # Create a Machine instance.
        #  (In __init__(), Try to load an existing model. If no model exists, train one).
        #  Use __init__() with open(). OR train a model and save it with save(). Fill in machine attributes using
        #  the model (loaded or created) and info(): self.name, self.timestamp, self.target, self.features, self.model

        # Try to load an existing model. Use open()
        filepath = os.path.join(PROJECT_ROOT, 'app', 'model.joblib')
        if os.path.exists(filepath):
            model = self.open(filepath)
            self.name = model
            self.timestamp = datetime.now()
            self.target = df["Rarity"]
            self.features = df.drop(columns=["Rarity"])
            self.model = model

            # Save the model labels/classes as part of the Machine object, for future use
            self.labels = ['Rank 0', 'Rank 1', 'Rank 2', 'Rank 3', 'Rank 4', 'Rank 5']

        else:
            # If no model exists, train one, then save with save().

            columns_to_drop = ['Timestamp', 'Damage', 'Name', 'Type']
            columns_to_drop = [col for col in columns_to_drop if col in df.columns]
            if columns_to_drop:
                df.drop(columns=columns_to_drop, inplace=True)

            self.target = df["Rarity"]
            self.features = df.drop(columns=["Rarity"])

            # Initializing the Random Forest Classifier
            self.model = RandomForestClassifier(random_state=42)

            # Fitting the model
            self.model.fit(self.features, self.target)

            # Save the trained model
            self.save(filepath)

            self.name = self.model
            self.timestamp = datetime.now()
            self.target = df["Rarity"]
            self.features = df.drop(columns=["Rarity"])

            # Save the labels/classes for future use
            self.labels = ['Rank 0', 'Rank 1', 'Rank 2', 'Rank 3', 'Rank 4', 'Rank 5']

    def __call__(self, pred_basis: DataFrame):
        prediction, *_ = self.model.predict(pred_basis)
        confidence = max(self.model.predict_proba(pred_basis)[0])
        return prediction, confidence

    def retrain(self, df):
        filepath = os.path.join(PROJECT_ROOT, 'app', 'model.joblib')

        columns_to_drop = ['Timestamp', 'Damage', 'Name', 'Type']
        columns_to_drop = [col for col in columns_to_drop if col in df.columns]
        if columns_to_drop:
            df.drop(columns=columns_to_drop, inplace=True)

        self.target = df["Rarity"]
        self.features = df.drop(columns=["Rarity"])

        # Initializing the Random Forest Classifier
        self.model = RandomForestClassifier(random_state=42)

        # Fitting the model
        self.model.fit(self.features, self.target)

        # Save the trained model
        self.save(filepath)

        self.name = self.model
        self.timestamp = datetime.now()
        self.target = df["Rarity"]
        self.features = df.drop(columns=["Rarity"])

        # Save the labels/classes for future use
        self.labels = ['Rank 0', 'Rank 1', 'Rank 2', 'Rank 3', 'Rank 4', 'Rank 5']

    def save(self, filepath):
        # Save the model to a file
        dump(self.model, filepath)

    @staticmethod
    def open(filepath):
        model = load(filepath)
        return model

    def info(self):
        model_info = f'Base Model: {self.name}\n<br>Timestamp: {self.timestamp.strftime("%Y-%m-%d %I:%M:%S %p")}'
        return model_info
