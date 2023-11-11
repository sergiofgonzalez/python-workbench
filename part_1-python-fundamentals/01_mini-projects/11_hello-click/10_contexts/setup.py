from setuptools import setup

setup(
    name="tool",
    version="0.1.0",
    py_modules=["tool"],
    install_requires=["Click"],
    entry_points={
        "console_scripts": [
            "tool = tool:cli"
        ]
    }
)