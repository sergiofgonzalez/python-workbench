from setuptools import setup

setup(
    name="toint",
    version="0.1.0",
    py_modules=["toint"],
    install_requires=["Click"],
    entry_points={
        "console_scripts": [
            "toint = toint:cli"
        ]
    }
)