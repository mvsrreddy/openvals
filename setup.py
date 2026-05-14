from setuptools import setup, find_packages

setup(
    name="openvals",
    version="0.1.5",
    packages=find_packages(),
    include_package_data=True,

    install_requires=[
        "numpy",
        "pandas",
        "scikit-learn",
        "typer",
        "rich"
    ],

    entry_points={
        "console_scripts": [
            "openvals=openvals.cli.app:main"
        ]
    }
)