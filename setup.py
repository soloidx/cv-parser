from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="cv_parser",
    version="0.5",
    packages=find_packages(),
    scripts=["cv_parser"],
    install_requires=[
        "pyyaml==5.3.1", "jinja2==2.11.2", "fpdf==1.7.2", "pillow==7.1.1"
    ],
    package_data={
        "example": ["*.yml", "*.jpg"],
        "renderers": ["*.ttf", "*.html", "*.css", "*.js"],
    },
    include_package_data=True,

    # metadata to display on PyPI
    author="Ider Delzo",
    author_email="soloidx@gmail.com",
    description="This package parses a Curriculum vitae yaml file and generates a pdf and web files",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords="resume cv, curriculum vitae",
    url="https://github.com/soloidx/cv-parser",
    project_urls={
        "Bug Tracker": "https://github.com/soloidx/cv-parser/issues",
        "Source Code": "https://github.com/soloidx/cv-parser",
    },
    classifiers=[
        "License :: OSI Approved :: MIT License"
    ]
)
