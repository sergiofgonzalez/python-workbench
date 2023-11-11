from setuptools import setup

setup(
    name="randfpck",
    version="0.1.0",
    py_modules=["randfpck"],
    install_requires=["Click"],
    entry_points={
        "console_scripts": [
            "randfpck = randfpck:cli"
        ]
    }
)