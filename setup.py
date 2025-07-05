from setuptools import setup, find_packages

setup(
    name='coggle',
    version='0.1.0',
    description='Automate Kaggle kernel runs and sync results via CLI',
    author='Siddharth Karmokar',
    packages=find_packages(),
    install_requires=[
        "pydantic>=2.0",
        "kaggle>=1.5.12",
    ],
    entry_points={
        'console_scripts': [
            'coggle=coggle.cli:main',
        ],
    },
    include_package_data=True,
    python_requires=">=3.8",
)
