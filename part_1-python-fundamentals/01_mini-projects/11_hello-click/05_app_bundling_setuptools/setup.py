from setuptools import setup

setup(
    name="appscript",
    version="0.1.0",
    py_modules=["yourscript"],
    install_requires=["Click"],
    entry_points={"console_scripts": ["appscript = appscript:cli"]},
)
