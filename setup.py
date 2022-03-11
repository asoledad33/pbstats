import setuptools

with open('requirements.txt') as f:
    required = f.read().splitlines()

DESCRIPTION = 'A package that extracts data from a json file and displays statistics'

setuptools.setup(
    name="pbstats",
    version="0.0.1",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    install_requires=required,
    python_requires='>=3.6',
)
