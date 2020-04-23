import pathlib
import shutil
from typing import Dict
from jinja2 import Environment, FileSystemLoader, select_autoescape

TEMPLATES_FOLDER = pathlib.Path(__file__).parent.joinpath(
    'templates').absolute()
THEMES_FOLDER = pathlib.Path(__file__).parent.joinpath(
    'themes').absolute()

DEFAULT_THEME = 'default'


def save_to_disk(render_text: str):
    output_dir = './output'
    filename = 'index.html'

    pathlib.Path(output_dir).mkdir(parents=True, exist_ok=True)

    with open(pathlib.Path(output_dir).joinpath(filename).absolute(),
              'w') as f:
        f.write(render_text)


def process_picture(pic_filename: str):
    if not pic_filename:
        return

    output_dir = './output/images'
    pathlib.Path(output_dir).mkdir(parents=True, exist_ok=True)

    dest = pathlib.Path(f'{output_dir}/{pic_filename}')

    if dest.exists():
        dest.unlink()
    shutil.copy(pic_filename, dest)


def insert_theme(theme_name: str = DEFAULT_THEME):
    css_dir = pathlib.Path('./output/css')
    js_dir = pathlib.Path('./output/js')

    if css_dir.exists():
        shutil.rmtree(css_dir.absolute())
    if js_dir.exists():
        shutil.rmtree(js_dir.absolute())

    shutil.copytree(f'{THEMES_FOLDER}/{theme_name}/css', css_dir.absolute())
    shutil.copytree(f'{THEMES_FOLDER}/{theme_name}/js', js_dir.absolute())


def render(cv_structure: Dict):
    env = Environment(loader=FileSystemLoader(TEMPLATES_FOLDER),
                      autoescape=select_autoescape(['html', 'xml']))

    template = env.get_template('main.html')
    save_to_disk(template.render(cv_data=cv_structure))

    process_picture(cv_structure['personal_info'].get('picture'))
    insert_theme()
