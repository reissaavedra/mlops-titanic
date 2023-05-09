from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score


class Metrics:
    def __init__(self,
                 y_train, y_valid,
                 y_pred_train, y_pred_valid):
        self.y_train = y_train
        self.y_valid = y_valid
        self.y_pred_train = y_pred_train
        self.y_pred_valid = y_pred_valid

    def get_metrics(self):
        return dict(
            accu_train=accuracy_score(self.y_train, self.y_pred_train),
            precission_train=precision_score(self.y_train, self.y_pred_train),
            recall_train=recall_score(self.y_train, self.y_pred_train),
            f1_train=f1_score(self.y_train, self.y_pred_train),
            accu_test=accuracy_score(self.y_valid, self.y_pred_valid),
            precission_test=precision_score(self.y_valid, self.y_pred_valid),
            recall_test=recall_score(self.y_valid, self.y_pred_valid),
            f1_test=f1_score(self.y_valid, self.y_pred_valid)
        )
