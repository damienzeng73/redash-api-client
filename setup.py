import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="redash-api-client",
    version="0.2.2",
    author="Damien Zeng",
    author_email="damnee562@gmail.com",
    description="Redash API Client",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/damnee562/redash-api-client",
    packages=setuptools.find_packages(),
    install_requires=['requests'],
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
