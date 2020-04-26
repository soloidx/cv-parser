# CV Parser

Create and parse a resume in YAML format.

## Dependencies:

- Pyyaml: for the parsing of the .yaml file.
- PyPDF: for the pdf creation.
- Pillow: for the image operation over the profile picture.
- Jinja2: for the creation of the web page resume.

## Installation:

You can install it using PIP:

    pip install cv-parser

## Usage:

In order to create the initial structure of the CV you can execute this command:

    cv_parser  generate
  
This will create `my_cv.yml` and `me.jpg` files.

Once you have edited this files you can do:

    cv_parser my_cv.yml

This will take the `my_cv.yml` file and generate the resume files into the
`output` folder.

Usually the `cv_parse` command generate a pdf and html file, if you only want
one of those you can run fo web:

    cv_parser --render-type web my_cv.yml

or

    cv_parser --render-type pdf my_cv.yml
  
for pdf creation.
