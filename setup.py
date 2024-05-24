from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

from JupyterExport import __version__ as version

setup(
    name="JupyterExport",
    version="0.1.7",
    author="Alan",
    author_email="alananalyst00@gmail.com",
    url='https://github.com/Alan-Analyst/JupyterExport',
    description="Convert .ipynb files to .pdf/.html using a simple graphical interface.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    include_package_data=True,
    package_data={
        'JupyterExport': ['assets/*.ico', 'assets/*.json'],  # Include all PNG and TXT files in the assets directory
    },
    python_requires='>=3.6',
    install_requires=[
        # List your project dependencies here
        'customtkinter',
        'nbformat',
        'nbconvert',
        'IPython',
        'Pygments'
    ],
    entry_points={
        'console_scripts': [
            'JupyterExport=JupyterExport.main:main', 'jupyterexport=JupyterExport.main:main',
            'JR=JupyterExport.main:main',
        ],
    },
)
