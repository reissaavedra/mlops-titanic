import numpy as np
import pandas as pd
from category_encoders import BinaryEncoder
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.preprocessing import OneHotEncoder


class NameColumnTransformer(BaseEstimator, TransformerMixin):
    """
    a general class for transforming Name, SibSp and Parch columns of Titanic dataset
    for using in the machine learning pipeline
    """

    def __init__(self):
        """
        constructor
        """
        # Will be used for fitting data
        self.titles_set = set()
        self.surname_set = set()
        # Titles captured from train data
        self.normal_titles_list = ["Mr", "Mrs", "Mme", "Miss", "Mlle", "Ms", "Master", "Dona"]
        self.titles_dict = {"Mr": ['Mr', 'Major', 'Jonkheer', 'Capt', 'Col', 'Don', 'Sir',
                                   'Rev'],
                            "Mrs": ['Mrs', 'Mme', 'Lady', 'Countess', 'Dona'],
                            "Miss": ['Miss', 'Mlle', 'Ms'],
                            "Master": ['Master'],
                            "Dr": ['Dr']}

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
        # Create Titles column
        if "title" in X_temp.columns:
            X_temp.drop("title", axis=1, inplace=True)
        else:
            pd.DataFrame.insert(X_temp, len(X_temp.columns), "title", "", False)

            # Get the index values
        index_values = X_temp.index.values.astype(int)

        # Set state (Add to: {titles_set, surname_set} attributes) of the object
        for i in index_values:

            # Get the name for the ith index
            name = X_temp.loc[i, 'name']
            # Get the number of followers for the ith index
            number_of_followers = X_temp.loc[i, 'sib_sp'] + X_temp.loc[i, 'parch']

            # Split the title from name
            if name.find('.'):
                title = name.split('.')[0].split()[-1]
                if title in self.titles_dict.keys():
                    X_temp.loc[i, 'title'] = title
                else:
                    X_temp.loc[i, 'title'] = np.NaN
                # Add title to titles_set to use in transform method
                self.titles_set.add(title)

            # Split the surname from name
            if name.find(','):
                surname = name.split(',')[0].split()[-1]
                # Add surname to surname_set to use in transform method
                if number_of_followers > 0:
                    self.surname_set.add(surname)
                    X_temp.loc[i, "family"] = surname

        # Title Encoding

        # Drop missing Title rows (Hi rank columns that are mapped to titles_dict keys)
        # so that no 'Title_' columns will appear in transform
        X_temp.dropna(axis="index", subset=['title'], inplace=True)

        # Apply one-hot encoding to the Title column.
        self.OH_encoder = OneHotEncoder(handle_unknown='ignore', sparse=False)
        # Get column names to use in transform.
        self.OH_encoder = self.OH_encoder.fit(X_temp[['title']])
        self.title_columns = self.OH_encoder.get_feature_names_out(['title'])

        # Family Encoding

        # Drop missing Family rows
        # so that no 'Family_' columns will appear in transform
        X_temp.dropna(axis="index", subset=['family'], inplace=True)

        # Apply binary encoding to the Family column.
        self.binary_encoder = BinaryEncoder(cols=['family'])
        self.binary_encoder = self.binary_encoder.fit(X_temp[['family']])

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

        # Create Titles column
        pd.DataFrame.insert(X_temp, len(X_temp.columns), "title", "", False)
        # Create Family column
        pd.DataFrame.insert(X_temp, len(X_temp.columns), "family", "", False)
        # Create Rank column
        pd.DataFrame.insert(X_temp, len(X_temp.columns), "rank", "", False)
        # Create Followers column
        pd.DataFrame.insert(X_temp, len(X_temp.columns), "followers", "", False)

        # Get the index values
        index_values = X_temp.index.values.astype(int)

        for i in index_values:
            # Get the name for the ith index
            name = X_temp.loc[i, 'name']
            # Get the number of followers for the ith index
            number_of_followers = X_temp.loc[i, 'sib_sp'] + X_temp.loc[i, 'parch']
            X_temp.loc[i, 'followers'] = number_of_followers

            # Split the title from name
            if name.find('.'):
                title = name.split('.')[0].split()[-1]
                if title in self.titles_set:
                    for key in self.titles_dict:
                        # Insert title
                        if title in self.titles_dict[key]:
                            X_temp.loc[i, 'title'] = key

                            # Insert rank
                        if title in self.normal_titles_list:
                            X_temp.loc[i, 'rank'] = "normal"
                        else:
                            X_temp.loc[i, 'rank'] = "high"
                else:
                    X_temp.loc[i, 'title'] = "other"
                    X_temp.loc[i, 'rank'] = "normal"

            # Split the surname from name
            if name.find(','):
                surname = name.split(',')[0].split()[-1]
                if surname in self.surname_set and number_of_followers > 0:
                    X_temp.loc[i, 'family'] = surname
                else:
                    X_temp.loc[i, 'family'] = "NA"

                    # Encoding Title
        encoded = self.OH_encoder.transform(X_temp[['title']])
        # convert arrays to a dataframe
        encoded = pd.DataFrame(encoded)
        # One-hot encoding removed index; put it back
        encoded.index = X_temp.index
        # Insert column names
        encoded.columns = self.title_columns
        encoded = encoded.astype('int64')
        # concating dataframes
        X_temp = pd.concat([X_temp, encoded], axis=1)

        # Encoding Family
        bin_encoded = self.binary_encoder.transform(X_temp[['family']])
        # convert arrays to a dataframe
        bin_encoded = pd.DataFrame(bin_encoded)
        # One-hot encoding removed index; put it back
        bin_encoded.index = X_temp.index
        bin_encoded = bin_encoded.astype('int64')
        # concating dataframes
        X_temp = pd.concat([X_temp, bin_encoded], axis=1)
        # We do not need Family anymore
        X_temp.drop("family", axis=1, inplace=True)

        # Encoding Rank
        X_temp['rank'] = X_temp['rank'].apply(lambda x: 1 if x == 'normal' else (0 if x == 'high' else None))
        # We do not need Name anymore
        X_temp.drop("name", axis=1, inplace=True)

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
