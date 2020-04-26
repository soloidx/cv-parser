from PIL import Image, ImageDraw
from typing import Dict
import pathlib

from fpdf import FPDF

RIGHT_TOP_MARGIN = 20

RESOURCES_FOLDER = pathlib.Path(__file__).parent.joinpath(
    'resources').absolute()


def add_fonts(pdf):
    pdf.add_font('pt_sans',
                 '',
                 f'{RESOURCES_FOLDER}/PTSans-Regular.ttf',
                 uni=True)

    pdf.add_font('pt_sans',
                 'B',
                 f'{RESOURCES_FOLDER}/PTSans-Bold.ttf',
                 uni=True)

    pdf.add_font('pt_sans',
                 'I',
                 f'{RESOURCES_FOLDER}/PTSans-Italic.ttf',
                 uni=True)

    pdf.add_font('questrial',
                 '',
                 f'{RESOURCES_FOLDER}/Questrial-Regular.ttf',
                 uni=True)


def insert_section_title(pdf, text):
    pdf.set_font('pt_sans', 'B', 18)
    pdf.ln(15)
    pdf.cell(40, 10, text)
    pdf.ln()


def insert_section_subtitile(pdf, text):
    pdf.set_font('questrial', '', 14)
    pdf.set_text_color(0, 0, 0)
    pdf.ln(2)
    pdf.cell(40, 10, text)
    pdf.ln(5)


def insert_3_level(pdf, text):
    pdf.set_font('pt_sans', 'B', 12)
    pdf.set_text_color(0, 0, 0)
    pdf.ln(7)
    pdf.cell(40, 10, text)
    pdf.ln(5)


def insert_project_item(pdf, project):
    pdf.set_font('questrial', '', 11)
    pdf.set_text_color(60, 150, 236)
    pdf.cell(0, 0, project.get('title'))
    pdf.set_text_color(0, 0, 0)
    pdf.ln(3)

    if project.get('description'):
        pdf.multi_cell(0, 4, project.get('description'))

    if project.get('platform'):
        pdf.ln(2)
        pdf.set_font('pt_sans', 'I', 11)
        pdf.set_text_color(150, 150, 150)
        pdf.multi_cell(0, 4, 'Platform: ' + project.get('platform'))
        pdf.set_text_color(0, 0, 0)

    if project.get('url'):
        pdf.ln(3)
        pdf.set_font('questrial', '', 9)
        pdf.set_text_color(25, 93, 158)
        pdf.cell(0, 0, project.get('url'))
        pdf.set_text_color(0, 0, 0)
    pdf.ln(5)


def save_to_disk(pdf_obj):
    output_dir = './output'
    filename = 'my_cv.pdf'

    pathlib.Path(output_dir).mkdir(parents=True, exist_ok=True)

    pdf_obj.output(pathlib.Path(output_dir).joinpath(filename).absolute(), 'F')


def check_page_break(pdf):
    offset = 250
    current_y = pdf.get_y()
    if current_y > offset:
        pdf.add_page()


def render_image(pdf, personal_info):
    filename = personal_info.get('picture')
    if filename is None:
        return ''

    im = Image.open(filename)
    im_w, im_h = im.size
    min_s = min(im.size)

    im = im.crop(((im_w - min_s) // 2, (im_h - min_s) // 2,
                  (im_w + min_s) // 2, (im_h + min_s) // 2))

    offset = 10

    mask = Image.new('L', im.size, 0)

    draw = ImageDraw.Draw(mask)
    draw.ellipse((offset, offset, im.size[0] - offset, im.size[1] - offset),
                 fill=255)

    im.putalpha(mask)
    new_filename = filename.split('.')[:-1]
    new_filename = '_'.join(new_filename)
    new_filename = f'{new_filename}_rendered.png'
    im.save(new_filename, quality=95)

    return new_filename


def render_header(pdf, data):
    image_filename = render_image(pdf, data.get('personal_info', {}))

    pdf.set_draw_color(60, 150, 236)
    if image_filename:
        pdf.image(image_filename, pdf.get_x() + 1, pdf.get_y() + 1, 30, 30)
        pdf.set_line_width(1)
        pdf.ellipse(pdf.get_x(), pdf.get_y(), 32, 32)
        pdf.set_left_margin(45)
        pdf.ln(5)
        im = pathlib.Path(image_filename)
        im.unlink()

    pdf.set_font('pt_sans', '', 24)
    full_name = f'%s %s' % (data['personal_info']['first_name'],
                            data['personal_info']['last_name'])
    pdf.cell(0, 10, full_name)
    pdf.ln()
    pdf.set_font('pt_sans', '', 18)
    pdf.set_text_color(150, 150, 150)
    pdf.cell(0, 10, data['personal_info']['title'])
    pdf.set_text_color(0, 0, 0)

    line_arg = [10, pdf.get_y() + 10, 120, 0.7, 'F']
    if image_filename:
        pdf.ln(8)
        line_arg[0] = 46
        line_arg[2] = 84

    pdf.set_fill_color(60, 150, 236)
    pdf.rect(*line_arg)

    pdf.set_left_margin(10)
    insert_section_title(pdf, 'Profile:')

    pdf.set_font('questrial', '', 11)
    pdf.multi_cell(120, 4, data['personal_info']['headline'])

    pdf.set_fill_color(17, 42, 75)
    pdf.rect(140, 0, 70, 297, 'F')


def render_experience(pdf, data):
    check_page_break(pdf)
    insert_section_title(pdf, 'Employment History:')

    works = [x.get('work') for x in data['professional_experience']]
    for work in works:
        check_page_break(pdf)
        insert_section_subtitile(pdf, work.get('job_title'))
        pdf.ln(2)
        pdf.set_font('pt_sans', 'I', 11)
        pdf.set_text_color(150, 150, 150)
        work_headline = '%s (%s)' % (work.get('place'), work.get('date'))
        pdf.cell(40, 6, work_headline)

        website = work.get('website')
        if website:
            pdf.ln(3)
            pdf.set_text_color(25, 93, 158)
            pdf.cell(40, 10, website)

        projects = work.get('projects', [])
        projects = [x.get('project') for x in projects]

        if projects:
            check_page_break(pdf)
            insert_3_level(pdf, 'Projects:')
            pdf.ln(6)

            pdf.set_left_margin(15)
            pdf.set_right_margin(80)
            for project in projects:
                check_page_break(pdf)
                insert_project_item(pdf, project)
            pdf.set_left_margin(10)


def render_core_formation(pdf, formation):
    pdf.set_left_margin(10)

    insert_section_title(pdf, 'Education:')

    if pdf.page_no() > 1:
        pdf.set_right_margin(10)

    courses = [x.get('course', {}) for x in formation]

    for course in courses:
        if course.get('institution'):
            pdf.set_font('pt_sans', 'I', 14)
            pdf.cell(0, 0, course.get('institution'), align='C')

        if course.get('location'):
            pdf.ln(5)
            pdf.set_font('questrial', '', 11)
            pdf.set_text_color(150, 150, 150)
            pdf.cell(0, 0, course.get('location'), align='C')

        if course.get('date'):
            pdf.ln(5)
            pdf.set_font('pt_sans', '', 11)
            pdf.set_text_color(150, 150, 150)
            pdf.cell(0, 0, str(course.get('date')), align='C')

        if course.get('title'):
            pdf.ln(7)
            pdf.set_font('questrial', '', 11)
            pdf.set_text_color(60, 150, 236)
            pdf.cell(0, 0, course.get('title'), align='C')

        pdf.set_text_color(0, 0, 0)

    pdf.set_text_color(0, 0, 0)


def render_complementary_formation(pdf, formation):
    pdf.set_left_margin(10)

    insert_section_title(pdf, 'Complementary Formation:')

    if pdf.page_no() > 1:
        pdf.set_right_margin(10)

    courses = [x.get('course', {}) for x in formation]

    for course in courses:
        if course.get('date'):
            pdf.ln(5)
            pdf.set_font('pt_sans', '', 11)
            pdf.set_text_color(150, 150, 150)
            pdf.cell(15, 0, str(course.get('date')))

        if course.get('institution'):
            pdf.set_font('pt_sans', 'I', 14)
            pdf.set_text_color(17, 42, 75)
            pdf.cell(0, 0, course.get('institution'))

        if course.get('title'):
            pdf.ln(5)
            pdf.set_font('questrial', '', 11)
            pdf.set_text_color(60, 150, 236)
            pdf.set_left_margin(25)
            pdf.cell(0, 0, course.get('title'))
            pdf.set_left_margin(10)

        pdf.set_text_color(0, 0, 0)
        pdf.ln(5)


def render_hobbies(pdf, hobbies):
    pdf.set_left_margin(10)

    insert_section_title(pdf, 'Hobbies:')

    if pdf.page_no() > 1:
        pdf.set_right_margin(10)

    for hobby in hobbies:
        if hobby.get('name'):
            pdf.ln(5)
            pdf.set_font('pt_sans', '', 11)
            pdf.set_text_color(150, 150, 150)
            pdf.cell(20, 0, str(hobby.get('name')))

        if hobby.get('description'):
            pdf.set_font('questrial', '', 11)
            pdf.set_text_color(60, 150, 236)
            pdf.set_left_margin(40)
            pdf.cell(0, 0, hobby.get('description'))
            pdf.set_left_margin(10)

        pdf.set_text_color(0, 0, 0)


def render_events(pdf, events):

    insert_section_title(pdf, 'Events: ')
    pdf.ln(10)

    if pdf.page_no() > 1:
        pdf.set_right_margin(10)

    for event in events:
        pdf.set_font('questrial', '', 11)
        pdf.set_text_color(17, 42, 75)
        pdf.set_left_margin(20)
        pdf.cell(0, 0, f'- {event}')
        pdf.set_left_margin(10)
        pdf.ln(5)

        pdf.set_text_color(0, 0, 0)


def render_references(pdf, references):
    pdf.set_left_margin(10)
    check_page_break(pdf)

    insert_section_title(pdf, 'References: ')
    pdf.ln(10)

    if pdf.page_no() > 1:
        pdf.set_right_margin(10)

    cont = 0

    for reference in references:
        initial_y = pdf.get_y()

        pdf.set_left_margin(cont * 63 + 10)

        pdf.set_font('pt_sans', '', 14)
        pdf.set_text_color(17, 42, 75)
        pdf.cell(63, 0, reference.get('name'), align='C')

        pdf.ln(4)

        if reference.get('title'):
            pdf.set_font('pt_sans', 'I', 11)
            pdf.set_text_color(150, 150, 150)
            pdf.cell(63, 0, reference.get('title'), align='C')
            pdf.ln(4)

        if reference.get('phone'):
            pdf.set_font('questrial', '', 11)
            pdf.set_text_color(60, 150, 236)
            pdf.cell(63, 0, str(reference.get('phone')), align='C')
            pdf.ln(4)

        if reference.get('email'):
            pdf.set_font('questrial', '', 11)
            pdf.set_text_color(60, 150, 236)
            pdf.cell(63, 0, reference.get('email'), align='C')
            pdf.ln(4)

        pdf.set_y(initial_y)

        cont += 1

        if cont % 3 == 0:
            pdf.ln(4)


def render_languages(pdf, languages):
    global RIGHT_TOP_MARGIN
    previous_y = pdf.get_y()

    pdf.set_left_margin(150)
    pdf.set_right_margin(10)
    pdf.set_y(RIGHT_TOP_MARGIN)
    pdf.set_font('questrial', '', 11)
    pdf.set_text_color(60, 150, 236)
    pdf.cell(50, 0, 'Languages:', align='C')
    pdf.ln(10)

    c_y = pdf.get_y()
    cont = 0

    for language in languages:
        pdf.set_text_color(255, 255, 255)
        pdf.set_font('pt_sans', '', 11)
        pdf.cell(25, 0, language.get('name'), align='C')
        pdf.ln(5)

        pdf.set_text_color(150, 150, 150)
        pdf.set_font('pt_sans', 'I', 10)
        pdf.cell(25, 0, language.get('level'), align='C')
        pdf.ln(6)

        cont += 1

        if cont % 2 == 0:
            pdf.set_left_margin(150)
            c_y = pdf.get_y()
        else:
            pdf.set_left_margin(175)
            pdf.set_y(c_y)

    pdf.ln(10)

    RIGHT_TOP_MARGIN = pdf.get_y()

    pdf.set_text_color(0, 0, 0)
    pdf.set_y(previous_y)
    pdf.set_left_margin(10)
    pdf.set_right_margin(10)


def render_skills(pdf, skills):
    global RIGHT_TOP_MARGIN
    previous_y = pdf.get_y()

    pdf.set_left_margin(150)
    pdf.set_right_margin(10)
    pdf.set_y(RIGHT_TOP_MARGIN)
    pdf.set_font('questrial', '', 11)
    pdf.set_text_color(60, 150, 236)
    pdf.cell(50, 0, 'Skills:', align='C')
    pdf.ln(10)

    for skill in skills:
        pdf.set_text_color(150, 150, 150)
        pdf.set_font('pt_sans', 'I', 10)
        pdf.cell(50, 0, skill.get('name'), align='L')
        pdf.ln(3)

        text = ', '.join(skill.get('list', []))
        pdf.set_text_color(255, 255, 255)
        pdf.set_font('pt_sans', '', 9)
        pdf.multi_cell(50, 5, text, align='C')
        pdf.ln(7)

    RIGHT_TOP_MARGIN = pdf.get_y()

    pdf.set_text_color(0, 0, 0)
    pdf.set_y(previous_y)
    pdf.set_left_margin(10)
    pdf.set_right_margin(10)


def render(cv_structure: Dict):
    pdf = FPDF('P', 'mm', 'A4')
    add_fonts(pdf)
    pdf.set_top_margin(20)
    pdf.add_page()

    render_header(pdf, cv_structure)

    if 'languages' in cv_structure.keys():
        render_languages(pdf, cv_structure['languages'])

    if 'skills' in cv_structure.keys():
        render_skills(pdf, cv_structure['skills'])

    if 'professional_experience' in cv_structure.keys():
        render_experience(pdf, cv_structure)

    if 'core_formation' in cv_structure.keys():
        render_core_formation(pdf, cv_structure['core_formation'])

    if 'complementary_formation' in cv_structure.keys():
        render_complementary_formation(pdf,
                                       cv_structure['complementary_formation'])

    if 'hobbies' in cv_structure.keys():
        render_hobbies(pdf, cv_structure['hobbies'])

    if 'events' in cv_structure.keys():
        render_events(pdf, cv_structure['events'])

    if 'references' in cv_structure.keys():
        render_references(pdf, cv_structure['references'])

    save_to_disk(pdf)
