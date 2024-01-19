from setuptools import setup

with open("README.md", encoding="utf-8") as file:
    read_me_description = file.read()

setup(
    name="piplib",
    version="0.1.1",
    author="Sergio F. Gonzalez",
    author_email="sergio.f.gonzalez@gmail.com",
    description="Demo library to illustrate editable builds",
    long_description=read_me_description,
    long_description_content_type="text/markdown",
    packages=["piplib"],
    include_package_data=True,
    install_requires=[],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
)
