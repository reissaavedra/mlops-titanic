import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin


class AgeColumnTransformer(BaseEstimator, TransformerMixin):
    def __init__(self):
        """
        constructor
        """
        # Will be used for fitting data
        self.titles_set = set()
        self.titles_dict = {}

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

        # Get the index values
        index_values = X_temp.index.values.astype(int)

        # Get all the titles from dataset
        for i in index_values:
            title = X_temp.loc[i, 'title']
            self.titles_set.add(title)

        # Calculate mean for all titles
        for title in self.titles_set:
            mean = self.calculate_mean_age(title, X_temp)
            self.titles_dict[title] = mean

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

        # If a passengers age is Nan replace it with the average value
        # of that title class. e.g. if that passenger is master use the
        # mean value calculated for the masters.
        for i in index_values:
            age = X_temp.at[i, 'age'].astype(float)
            if np.isnan(age):
                title = X_temp.loc[i, 'title']
                X_temp.loc[i, 'age'] = round(self.titles_dict.get(title), 2)

        X_temp.drop("title", axis=1, inplace=True)

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

    def calculate_mean_age(self, title, X):

        # Make a copy to avoid changing original data
        X_temp = X.copy()

        title_X = X_temp[[title in x for x in X_temp['title']]][X_temp["age"].notnull()]
        return title_X["age"].mean()
