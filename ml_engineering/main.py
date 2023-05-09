import pandas as pd
from loguru import logger
from sklearn.metrics import accuracy_score

from app.database import db
from app.ml_engineering.data_loader.DataLoader import DataLoader
from app.ml_engineering.model.logistic_regression_model import LogisticRegressionModel
from app.ml_engineering.pipeline.feature_pipeline.feature_pipeline import FeaturePipeline
from app.ml_engineering.pipeline.training_pipeline.train_pipeline import TrainingPipeline

warnings.simplefilter(action='ignore')
experiment_name = "my-experiment"
numerical_cols = ['p_class', 'fare']
categorical_cols = ['sex', 'embarked']


def step_previous():
    data_loader = DataLoader(db)
    query_titanic_train_dataset = "SELECT * FROM titanic_train"
    titanic_train_dataset = data_loader.get_data(query_titanic_train_dataset)
    titanic_train_dataset = data_loader.remove_columns(titanic_train_dataset, columns=['created_at', 'ticket'])
    return data_loader.train_test_split(titanic_train_dataset,
                                        label='survived',
                                        random_state=2)


def start_application():
    X_train, X_valid, y_train, y_valid = step_previous()
    feature_pipeline = FeaturePipeline(numerical_cols=numerical_cols, categorical_cols=categorical_cols) \
        .get_pipeline()

    X_valid_eval = X_valid.copy()

    X_valid_eval = feature_pipeline.fit(X_train, y_train).transform(X_valid_eval)

    fit_params = {"model__early_stopping_rounds": 50,
                  "model__eval_set": [(X_valid_eval, y_valid)],
                  "model__verbose": True,
                  "model__eval_metric": "error"}

    # my_model = XGBClassifier(
    #     )

    log_reg_params = {
        'solver': 'lbfgs'
    }
    log_reg_model = LogisticRegressionModel(**log_reg_params)

    train_pipeline = TrainingPipeline(feature_pipeline, log_reg_model).get_training_pipeline()

    train_pipeline.fit(X_train, y_train)

    predictions = train_pipeline.predict(X_valid)

    score = accuracy_score(y_valid, predictions)

    logger.info("Score: {}".format(score))

    xgboost_params = dict(learning_rate=0.01,
                          n_estimators=40,
                          max_depth=5,
                          min_child_weight=1,
                          gamma=0,
                          subsample=0.8,
                          colsample_bytree=0.8,
                          seed=42)

    # xgboost_model = XGBClassifier(**xgboost_params)

    # cv_pipeline = Pipeline(steps=[('feature_pipeline', feature_pipeline),
    #                               ('model', cv_model)
    #                               ])

    # scores = cross_val_score(cv_pipeline, X_train, y_train,
    #                          cv=5,
    #                          scoring='accuracy')

    # print("Accuracy of the folds:\n", scores)
    # print("\nmean:\n", scores.mean())
    # print("std:\n", scores.std())

    # Preprocessing of training data, fit model
    # cv_pipeline.fit(X_train, y_train)

    # Get predictions
    # predictions = cv_pipeline.predict(X_valid)

    # Evaluate the model
    # score = accuracy_score(y_valid, predictions)

    # print("Score: {}".format(score))

    # Preprocessing of training data, fit model
    # cv_pipeline.fit(X, y)

    # Get predictions
    # preds = cv_pipeline.predict(X_test)


def start_application_with_mlflow():
    from atom import ATOMClassifier
    logger.info("Starting project")
    X_train, X_valid, y_train, y_valid = step_previous()
    feature_pipeline = FeaturePipeline(numerical_cols=numerical_cols, categorical_cols=categorical_cols) \
        .get_pipeline()
    log_reg_params = dict(solver='lbfgs')
    log_reg_model = LogisticRegressionModel(**log_reg_params)
    # train_pipeline = TrainingPipeline(feature_pipeline, log_reg_model).get_training_pipeline()

    x = feature_pipeline.fit(X_train, y_train).transform(X_train)
    logger.info(x.shape)
    logger.info(y_train.shape)

    X = pd.read_csv("https://raw.githubusercontent.com/tvdboom/ATOM/master/examples/datasets/weatherAUS.csv")

    atom = ATOMClassifier(X, y="RainTomorrow", n_rows=1000, verbose=2, experiment='a_test')
    atom.impute(strat_num="median", strat_cat="most_frequent")
    atom.encode(strategy="Target", max_onehot=8)
    atom.run(models=["LDA", "AdaB"], metric="auc", n_trials=10)

    # with mlflow.start_run(run_name="run_test") as run:
    #     # train_pipeline.fit(X_train, y_train)
    #
    #
#
    #     pred_x_train = train_pipeline.predict(X_train)
    #     score_x_train = accuracy_score(y_train, pred_x_train)
#
        #pred_x_valid = train_pipeline.predict(X_valid)
    #     score_x_valid = accuracy_score(y_valid, pred_x_valid)

    #     mlflow.log_metric("train_score", score_x_train)
    #     mlflow.log_metric("valid_score", score_x_valid)
    #     mlflow.log_params(log_reg_params)

    #     mlflow.sklearn.log_model(sk_model=train_pipeline,
     #                             artifact_path="log_reg_model",
    #                              registered_model_name="sk-learn-log-reg-model-v1",
    #                              )

if __name__ == '__main__':
    start_application_with_mlflow()
