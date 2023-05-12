from abc import ABC, abstractmethod


class InferenceProcess(ABC):
    def execute(self):
        self.get_data()
        self.feature_pipeline()
        self.run_inference()
        # self.save_predictions()

    @abstractmethod
    def get_data(self):
        raise NotImplementedError()

    @abstractmethod
    def feature_pipeline(self):
        raise NotImplementedError()

    @abstractmethod
    def run_inference(self):
        raise NotImplementedError()

