from setuptools import setup

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name='ml_titanic',
    version='0.1',
    py_modules=['ml_engineering', 'etl', 'database',  'configuration'],
    install_requires=requirements,
    entry_points='''
        [console_scripts]
        etl=etl.main:main
        [console_scripts]
        train=ml_engineering.pipeline.training_pipeline.main:main
        [console_scripts]
        features=ml_engineering.pipeline.feature_pipeline.main:main
        [console_scripts]
        inference=ml_engineering.pipeline.inference_pipeline.main:main
    ''',
)
