from abc import ABC, abstractmethod

from sklearn.metrics import (accuracy_score, f1_score, precision_score,
                             recall_score)


class MetricsStrategy(ABC):
    @property
    @abstractmethod
    def metric_name(self):
        raise NotImplementedError

    @abstractmethod
    def calculate(self, predictions, labels):
        raise NotImplementedError


class AccuracyStrategy(MetricsStrategy):
    @property
    def metric_name(self):
        return 'accuracy'

    def calculate(self, predictions, labels):
        return accuracy_score(labels, predictions)


class PrecisionStrategy(MetricsStrategy):
    @property
    def metric_name(self):
        return 'precision'

    def calculate(self, predictions, labels):
        return precision_score(labels, predictions)


class RecallStrategy(MetricsStrategy):

    @property
    def metric_name(self):
        return 'recall'

    def calculate(self, predictions, labels):
        return recall_score(labels, predictions)


class F1ScoreStrategy(MetricsStrategy):
    @property
    def metric_name(self):
        return 'f1-score'

    def calculate(self, predictions, labels):
        return f1_score(labels, predictions)


class MetricsCalculator:
    def __init__(self):
        self.strategy = None

    def set_strategy(self, strategy: MetricsStrategy):
        self.strategy: MetricsStrategy = strategy

    def calculate_metrics(self, predictions, labels):
        return self.strategy.calculate(predictions, labels)


class MetricsStrategyIterator:
    def __init__(self):
        self.strategies = []
        self.calculator = MetricsCalculator()

    def add_strategy(self, strategy):
        self.strategies.append(strategy)

    def calculate_metrics(self, predictions, y, tag):
        metrics = {}
        for strategy in self.strategies:
            self.calculator.set_strategy(strategy)
            metric_value = self.calculator.calculate_metrics(predictions, y)
            metrics[f'{strategy.metric_name}-{tag}'] = metric_value
        return metrics
