import pandas as pd
from loguru import logger
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder


class CabinColumnTransformer(BaseEstimator, TransformerMixin):
    """
    a general class for transforming cabin column of Titanic dataset for using in the machine
    learning pipeline
    """

    def __init__(self):
        """
        constructor
        """
        # Will be used for fitting data
        self.cabin_set = set()

    def fit(self, X, y=None, **kwargs):
        """
        an abstract method that is used to fit the step and to learn by examples
        :param X: features - Dataframe
        :param y: target vector - Series
        :param kwargs: free parameters - dictionary
        :return: self: the class object - an instance of the transformer - Transformer
        """
        '''Fits the titles, family and rank from Names Column'''

        # Make a copy to avoid changing original data
        X_temp = X.copy()

        # Imputation on X_temp_imputed
        imputer = SimpleImputer(strategy='constant', fill_value="NaN")
        X_temp_imputed = pd.DataFrame(imputer.fit_transform(X_temp[['cabin']]))
        # Imputation removed column names; put them back
        X_temp_imputed.columns = X_temp[['cabin']].columns

        X_temp_imputed.index = X_temp[['cabin']].index

        # Get the index values
        index_values = X_temp.index.values.astype(int)

        # For each cabin
        for i in index_values:
            cabin = X_temp_imputed.loc[i, 'cabin']
            X_temp_imputed.loc[i, 'cabin'] = cabin[0]
            self.cabin_set.add(cabin[0])

        # cabin Encoding

        # Apply one-hot encoding to the cabin column.
        self.OH_encoder = OneHotEncoder(handle_unknown='ignore', sparse=False)
        # Get column names to use in transform.
        self.OH_encoder = self.OH_encoder.fit(X_temp_imputed[['cabin']])
        self.cabin_columns = self.OH_encoder.get_feature_names_out(['cabin'])

        return self

    def transform(self, X, y=None, **kwargs):
        """
        an abstract method that is used to transform according to what happend in the fit method
        :param X: features - Dataframe
        :param y: target vector - Series
        :param kwargs: free parameters - dictionary
        :return: X: the transformed data - Dataframe
        """
        '''Transforms the titles and family from Names Column'''

        # Make a copy to avoid changing original data
        X_temp = X.copy()

        # Get the index values
        index_values = X_temp.index.values.astype(int)

        # Imputation on X_imputed
        imputer = SimpleImputer(strategy='constant', fill_value="NaN")
        X_imputed = pd.DataFrame(imputer.fit_transform(X_temp[['cabin']]))
        # Imputation removed column names; put them back
        X_imputed.columns = X_temp[['cabin']].columns
        X_imputed.index = X_temp[['cabin']].index

        for i in index_values:
            cabin = X_imputed.loc[i, 'cabin']
            if cabin[0] in self.cabin_set:
                X_imputed.loc[i, 'cabin'] = cabin[0]
            else:
                X_imputed.loc[i, 'cabin'] = "N"
        X_temp.drop("cabin", axis=1, inplace=True)

        # concating dataframes
        X_temp = pd.concat([X_temp, X_imputed], axis=1)

        # Encoding cabin
        encoded = self.OH_encoder.transform(X_imputed[['cabin']])
        # convert arrays to a dataframe
        encoded = pd.DataFrame(encoded)
        # One-hot encoding removed index; put it back
        encoded.index = X_imputed.index
        # Insert column names
        encoded.columns = self.cabin_columns
        encoded = encoded.astype('int64')
        # concating dataframes
        X_temp = pd.concat([X_temp, encoded], axis=1)

        X_temp.drop("cabin", axis=1, inplace=True)

        return X_temp

    def fit_transform(self, X, y=None, **kwargs):
        """
        perform fit and transform over the data
        :param X: features - Dataframe
        :param y: target vector - Series
        :param kwargs: free parameters - dictionary
        :return: X: the transformed data - Dataframe
        """
        self = self.fit(X, y)
        return self.transform(X, y)
