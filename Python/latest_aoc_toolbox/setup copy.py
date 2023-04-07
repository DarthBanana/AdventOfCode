
import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name='aoctoolbox',
    version='0.0.2',
    author='Randy Aull',
    author_email='randyaull@hotmail.com',
    description='My Advent of Code Toolbox',
    long_description=long_description,
    long_description_content_type="text/markdown",
    license='MIT',
    packages=['.'],
    install_requires=['pygame','networkx'],
)