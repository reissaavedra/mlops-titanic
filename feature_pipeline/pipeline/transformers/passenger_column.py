from sklearn.base import BaseEstimator, TransformerMixin


class PassengerColumnTransformer(BaseEstimator, TransformerMixin):
    def fit(self, X, y=None):
        return self

    def transform(self, X, y=None):
        return X.drop(['passenger_id'], axis=1)
