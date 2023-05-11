class ETLConfig:
    def __init__(self):
        self.database = None
        self.api = None
        self.pipeline = []
        self.fill_empty = False
        self.union = False
        self.alembic = False

    def set_build_alembic(self, alembic):
        self.alembic = alembic
        return self

    def set_api(self, api):
        self.api = api
        return self

    def add_transformation_step(self, step):
        self.pipeline.append(step)
        return self

    def set_database(self, db):
        self.database = db
        return self

    def set_fill_empty(self, bool_value):
        self.fill_empty = bool_value
        return self

    def set_union(self, bool_value):
        self.union = bool_value
        return self

    def build(self):
        return self
