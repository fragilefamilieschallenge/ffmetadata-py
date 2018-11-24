import setuptools
import ff

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ffmetadata-py",
    version=ff.__version__,
    author="Vineet Bansal",
    author_email="vineetb@princeton.edu",
    description="Python wrapper for The Fragile Families Metadata API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/fragilefamilieschallenge/ffmetadata-py",
    packages=['ff'],
	install_requires=['simplejson','urllib','requests'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)