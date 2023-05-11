from typing import List

import pandas as pd
from sklearn.model_selection import train_test_split
from sqlalchemy.orm import Session


class DataLoader:
    def __init__(self, db: Session):
        self.db = db

    def get_data(self, query: str) -> pd.DataFrame:
        result = self.db.execute(query)
        return pd.DataFrame(result.fetchall(), columns=result.keys())

    @staticmethod
    def remove_columns(df: pd.DataFrame, columns: List[str]):
        return df.drop(columns, axis=1)

    def train_test_split(self, df: pd.DataFrame, label: str, random_state=2):
        y = df[label]
        X = self.remove_columns(df, [label])
        X_train, X_valid, y_train, y_valid = train_test_split(X, y, random_state=random_state, test_size=0.2)
        return X_train, X_valid, y_train, y_valid
