from setuptools import find_packages, setup

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name='ml_titanic',
    version='0.1',
    packages=find_packages(),
    py_modules=['etl', 'database',  'configuration',
                'feature_pipeline', 'training_pipeline', 'inference_pipeline'],
    install_requires=requirements,
    entry_points='''
        [console_scripts]
        etl=etl.main:main
        [console_scripts]
        train=training_pipeline.main:main
        [console_scripts]
        features=feature_pipeline.main:main
        [console_scripts]
        inference=inference_pipeline.main:main
    ''',
)
