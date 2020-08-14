import pathlib
import re
import setuptools

# long_description
with open("README.md", "r") as fh:
    long_description = fh.read()


# version
directory = pathlib.Path(__file__).parent.resolve()
init_path = directory.joinpath('pathwayParameterAdvising', '__init__.py')
text = init_path.read_text()
pattern = re.compile(r"^__version__ = ['\"]([^'\"]*)['\"]", re.MULTILINE)
version = pattern.search(text).group(1)


setuptools.setup(
    # Package details
    name="pathwayParameterAdvising",
    version=version,
    description="Parameter advising for biological pathway reconstruction algorithms.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/gitter-lab/pathway-parameter-advising",

    #Author Details
    author="Chris Magnano",
    author_email="chrismagnano@gmail.com",


    #Package Topics
    keywords = "pathway-finding parameter-advising pathway-reconstruction biological-pathway graphlet",
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering :: Bio-Informatics',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.6',
        "License :: OSI Approved :: MIT License",
        "Operating System :: Unix ",
        'Operating System :: MacOS :: MacOS X'
    ],
    python_requires='>=3.6',
    packages=setuptools.find_packages(),
    install_requires=[
        'numpy',
        'networkx',
        'requests',
    ],

    include_package_data=True,
)
