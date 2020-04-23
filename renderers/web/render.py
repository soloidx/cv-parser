import pathlib
from typing import Dict
from jinja2 import Environment, FileSystemLoader, select_autoescape

TEMPLATES_FOLDER = pathlib.Path(__file__).parent.joinpath(
    'templates').absolute()
print(TEMPLATES_FOLDER)


def render(cv_structure: Dict):
    env = Environment(loader=FileSystemLoader(TEMPLATES_FOLDER),
                      autoescape=select_autoescape(['html', 'xml']))

    template = env.get_template('main.html')
    print(template.render())
