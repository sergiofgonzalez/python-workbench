from setuptools import setup

setup(
    name="hellouser",
    version="0.1.0",
    py_modules=["hellouser"],
    install_requires=["Click"],
    entry_points={
        "console_scripts": [
            "hellouser = hellouser:hello"
        ]
    }
)