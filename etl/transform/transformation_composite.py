# Composite Pattern - Composite Transformation Step
class CompositeTransformationStep:
    def __init__(self):
        self.steps = []

    def add_step(self, step):
        self.steps.append(step)

    def transform(self, data):
        for step in self.steps:
            data = step.transform(data)
        return data
