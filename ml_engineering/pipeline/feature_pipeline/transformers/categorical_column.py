import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin


class CategoricalColumnTransformer(BaseEstimator, TransformerMixin):
    sex_dict = {'male': 0, 'female': 1}

    def fit(self, X, y=None):
        return self

    def transform(self, X, y=None):
        X['sex'] = [self.sex_dict[g] for g in X['sex']]

        X = pd.get_dummies(X, prefix="embarked",
                           columns=["embarked"],
                           drop_first=True)
        return X
