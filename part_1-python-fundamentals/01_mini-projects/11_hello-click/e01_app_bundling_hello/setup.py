from setuptools import setup

setup(
    name="hello_cli_app",
    version="0.1.0",
    py_modules=["main"],
    install_requires=["Click"],
    entry_points={
        "console_scripts": [
            "hello = main:cli_app"
        ]
    }
)