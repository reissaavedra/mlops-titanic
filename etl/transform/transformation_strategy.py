# Strategy Pattern - Transformation Strategies
import numpy as np
import pandas as pd


class TransformationStrategy:
    def transform(self, data):
        raise NotImplementedError()


class FillEmptyStrategy(TransformationStrategy):
    def transform(self, data):
        # Fill empty strings
        data['Age'] = data['Age'].replace(np.nan, None)
        data['Cabin'] = data['Cabin'].replace(np.nan, 'N')
        data['Fare'] = data['Fare'].replace(np.nan, 100.0)
        data['Embarked'] = data['Embarked'].replace(np.nan, 'C')
        data['Survived'] = data['Survived'].replace(np.nan, -1)
        return data


class UnionStrategy(TransformationStrategy):
    def transform(self, data_list):
        # Perform union operation on the list of DataFrames
        union_df = pd.concat(data_list)
        return union_df
