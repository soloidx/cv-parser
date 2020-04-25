from typing import Dict
import pathlib

from fpdf import FPDF

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
    pdf.ln(8)


def save_to_disk(pdf_obj):
    output_dir = './output'
    filename = 'my_cv.pdf'

    pathlib.Path(output_dir).mkdir(parents=True, exist_ok=True)

    pdf_obj.output(pathlib.Path(output_dir).joinpath(filename).absolute(), 'F')


def render_header(pdf, data):
    pdf.set_fill_color(17, 42, 75)
    pdf.rect(140, 0, 70, 297, 'F')

    pdf.set_font('pt_sans', '', 24)
    full_name = f'%s %s' % (data['personal_info']['first_name'],
                            data['personal_info']['last_name'])
    pdf.cell(40, 10, full_name)
    pdf.ln()
    pdf.set_font('pt_sans', '', 18)
    pdf.cell(40, 10, data['personal_info']['title'])

    insert_section_title(pdf, 'Profile:')

    pdf.set_font('questrial', '', 11)
    pdf.cell(40, 10, data['personal_info']['headline'])


def render_experience(pdf, data):
    insert_section_title(pdf, 'Employment History:')

    works = [x.get('work') for x in data['professional_experience']]
    for work in works:
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
            insert_3_level(pdf, 'Projects:')
            pdf.ln(6)

            pdf.set_left_margin(15)
            pdf.set_right_margin(80)
            for project in projects:
                insert_project_item(pdf, project)
            pdf.set_left_margin(10)


def render_core_formation(pdf, formation):
    pdf.set_left_margin(10)

    insert_section_title(pdf, 'Education:')
    pdf.ln(10)

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
        pdf.ln(10)

    pdf.set_text_color(0, 0, 0)


def render_complementary_formation(pdf, formation):
    pdf.set_left_margin(10)

    insert_section_title(pdf, 'Complementary Formation:')
    pdf.ln(10)

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
    pdf.ln(10)

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
    pdf.set_left_margin(10)

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
    print(references)
    pdf.set_left_margin(10)

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


def render(cv_structure: Dict):
    pdf = FPDF('P', 'mm', 'A4')
    add_fonts(pdf)
    pdf.add_page()

    render_header(pdf, cv_structure)
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

    print(cv_structure.keys())
    save_to_disk(pdf)
