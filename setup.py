import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pyside2-kit",
    version="0.0.1",
    author="Daniele Bernardini",
    author_email="bdcreations@gmail.com",
    description="A small example package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://https://github.com/DanieleBerna/pyside2-kit",
    packages=setuptools.find_packages(),
    install_requires=["PySide2"],

    # Package Data
    include_package_data=True,
    package_data={
        'pyside2-kit': ["resources/*.png", "resources/*.txt"]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)
