from abc import ABC, abstractmethod


class FeatureProcess(ABC):
    def execute(self):
        self.pre_process_data()
        self.execute_feature_pipeline()

    @abstractmethod
    def pre_process_data(self):
        raise NotImplementedError()

    @abstractmethod
    def execute_feature_pipeline(self):
        raise NotImplementedError()
