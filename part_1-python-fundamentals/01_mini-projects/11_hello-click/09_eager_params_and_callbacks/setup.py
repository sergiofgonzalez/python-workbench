from setuptools import setup

setup(
    name="hello-ver",
    version="0.1.0",
    py_modules=["hellover"],
    install_requires=["Click"],
    entry_points={
        "console_scripts": [
            "hello-ver = hellover:hello"
        ]
    }
)