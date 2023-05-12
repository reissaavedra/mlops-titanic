from abc import ABC, abstractmethod


class TrainingProcess(ABC):
    def __init__(self):
        self.data = None
        self.model = None
        self.config = None

    def execute(self):
        self.get_data()
        self.training_pipeline()
        self.evaluate_metrics()

    @abstractmethod
    def get_data(self):
        raise NotImplementedError()

    @abstractmethod
    def training_pipeline(self):
        raise NotImplementedError()

    @abstractmethod
    def evaluate_metrics(self):
        raise NotImplementedError()
