from setuptools import setup, find_packages
setup(
    name="cv_parser",
    version="0.1",
    packages=find_packages(),
    scripts=["cv_parser"],
    install_requires=[
        "pyyaml==5.3.1", "jinja2==2.11.2", "fpdf==1.7.2", "pillow==7.1.1"
    ],
    package_data={
        "example": ["*.yml", "*.jpg"],
        "renderers": ["*.ttf", "*.html", "*.css", "*.js"],
    },

    # metadata to display on PyPI
    author="Ider Delzo",
    author_email="soloidx@gmail.com",
    description="This package parses a Curriculum vitae yaml file and generates a pdf and web files",
    keywords="resume cv, curriculum vitae",
    url="https://github.com/soloidx/cv-parser",
    project_urls={
        "Bug Tracker": "https://github.com/soloidx/cv-parser/issues",
        "Source Code": "https://github.com/soloidx/cv-parser",
    },
    classifiers=[
        "License :: OSI Approved :: Python Software Foundation License"
    ]
)
