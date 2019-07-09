import json
import svgwrite
import pyqrcode
from reportlab.graphics import renderPDF
from reportlab.pdfgen import canvas
from svglib.svglib import svg2rlg
import os
import random
from reportlab.platypus import SimpleDocTemplate, Image
from reportlab.lib.units import inch


def setup_questions():
    questions = []
    d = dict()
    d['q'] = 'Wie is de teamleider van TEAT?'
    d['a'] = 'Donald duck'
    d['b'] = 'Michiel'
    d['c'] = 'Jan Smit'
    d['d'] = 'Wybo'
    d['ans'] = 'b'
    questions.append(d)

    e = dict()
    e['q'] = 'Wie is de teamleider van Aqua?'
    e['a'] = 'Donald duck'
    e['b'] = 'Pien'
    e['c'] = 'Jan Smit'
    e['d'] = 'Neptunes'
    e['ans'] = 'd'
    questions.append(e)

    with open('question.txt', 'w') as f:
        f.write(json.dumps(questions, sort_keys=True, indent=4))


def read_teamnames(in_file):
    teams = []
    with open(in_file, 'r') as f:
        for data in f.readlines():
            teams.append(data.strip())
    return teams


def process_teamnames(in_file, out_file):
    teams = read_teamnames(in_file)

    print('Number of teams: ' + str(len(teams)))
    print('Number of unique teams: ' + str(len(list(set(teams)))))
    # print('Teams: ' + ' '.join(teams))

    sorted_teams = list(sorted(set(teams)))
    with open(out_file, 'w') as f:
        f.write('\n'.join(sorted_teams))

    return sorted_teams


def qr_svg(dwg, qr, x, y, size):
    svg = dwg.add(dwg.g(stroke='none', fill='black'))
    vals = qr.split('\n')
    for dy in range(len(vals)):
        line = vals[dy]
        for dx in range(len(line)):
            if line[dx] == '1':
                insert = (x + size * dx, y + size * dy)
                svg.add(svgwrite.shapes.Rect(insert=insert, size=(size, size)))


def create_page(team, question):
    width = 600
    height = 700
    font_size_big = 22
    font_size_small = 10

    dwg = svgwrite.Drawing('teamnamen_logo/' + team + '.svg', (width, height), debug=True)

    lines = dwg.add(dwg.g(stroke_width=2, stroke='black', fill='none'))
    line_offset = 50
    lines.add(dwg.line(start=(line_offset, 0.5 * height), end=(width - line_offset, 0.5 * height)))
    lines.add(dwg.line(start=(0.5 * width, line_offset), end=(0.5 * width, height - line_offset)))

    paragraph = dwg.add(dwg.g(font_size=font_size_big, style='font-family:TESLAFONT;'))
    team_left = 0.3*width
    team_right = 0.7*width
    team_top = 0.0*height
    team_bottom = 0.55*height
    paragraph.add(dwg.text(team, (team_left, team_top), text_anchor='middle'))
    paragraph.add(dwg.text(team, (team_right, team_top), text_anchor='middle'))
    paragraph.add(dwg.text(team, (team_left, team_bottom), text_anchor='middle'))
    paragraph.add(dwg.text(team, (team_right, team_bottom), text_anchor='middle'))

    # QR code
    qr = pyqrcode.create('jambo:' + team + ':' + question['ans'], error='H')
    qr_svg(dwg, qr.text(), 0.04 * width, 0.0 * height, 8)

    # Question
    question_head = dwg.add(dwg.g(font_size=font_size_big, style='font-family:TESLAFONT;'))
    question_head.add(dwg.text('Vraag: ', (0.7 * width, 0.1 * height), text_anchor='middle'))
    question_text = dwg.add(dwg.g(font_size=font_size_small, style='font-family:TESLAFONT;'))
    question_text.add(dwg.text(question['q'], (0.7 * width, 0.2 * height), text_anchor='middle'))

    # Answer
    ans_head = dwg.add(dwg.g(font_size=font_size_big, style='font-family:TESLAFONT;'))
    antwoord_left = 0.15 * width
    ans_head.add(dwg.text('Antwoord:', (antwoord_left, 0.65 * height)))

    ans_text = dwg.add(dwg.g(font_size=font_size_small, style='font-family:TESLAFONT;'))
    ans_text.add(dwg.text('A: ' + question['a'], (antwoord_left, 0.7 * height)))
    ans_text.add(dwg.text('B: ' + question['b'], (antwoord_left, 0.75 * height)))
    ans_text.add(dwg.text('C: ' + question['c'], (antwoord_left, 0.8 * height)))
    ans_text.add(dwg.text('D: ' + question['d'], (antwoord_left, 0.85 * height)))

    # Color
    color = {'a': 'Rood', 'b': 'Groen', 'c': 'Geel', 'd': 'Oranje'}
    color_text = dwg.add(dwg.g(font_size=font_size_big, style='font-family:TESLAFONT;'))
    color_text.add(dwg.text('Kleur: ' + color[question['ans']], (0.7 * width, 0.75 * height), text_anchor='middle'))

    # Hints
    hint_text = dwg.add(dwg.g(font_size=font_size_small, style='font-family:TESLAFONT;'))
    hint_left = 0.13 * width
    hint_right = 0.53 * width
    hint_top = 0.45 * height
    hint_bottom = 0.95 * height
    next_line = 12

    hint_text.add(dwg.text(f'Vind van je team {team}:', (hint_left, hint_top)))
    hint_text.add(dwg.text('vraag, antwoord & kleur', (hint_left, hint_top + next_line)))

    hint_text.add(dwg.text(f'Vind van je team {team}:', (hint_right, hint_top)))
    hint_text.add(dwg.text('QR, antwoord & kleur', (hint_right, hint_top + next_line)))

    hint_text.add(dwg.text(f'Vind van je team {team}:', (hint_left, hint_bottom)))
    hint_text.add(dwg.text('QR, vraag & kleur', (hint_left, hint_bottom + next_line)))

    hint_text.add(dwg.text(f'Vind van je team {team}:', (hint_right, hint_bottom)))
    hint_text.add(dwg.text('QR, vraag & antwoord', (hint_right, hint_bottom + next_line)))
    dwg.save()


with open('question.txt', 'r', encoding="utf8") as f:
    questions = json.load(f)

for q in questions:
    print(q['q'] + ' -> ' + q[q['ans']])
print('Aantal vragen: ' + str(len(questions)))
quit()

teams = read_teamnames('teamnamen sorted.txt')
page_number = 0
for t in teams:
    create_page(t.upper(), questions[page_number % len(questions)])
    page_number += 1

save_dir = 'teamnamen_logo/'
files = os.listdir(save_dir)
random.shuffle(files)

my_canvas = canvas.Canvas('svg_on_canvas.pdf')
for f in files:
    my_canvas.drawImage('background.png', 5, 10)  # Who needs consistency?

    drawing = svg2rlg(save_dir + f)
    renderPDF.draw(drawing, my_canvas, 0, 40)

    my_canvas.showPage()
    print(f)
my_canvas.save()

# my_canvas = canvas.Canvas('svg_on_canvas.pdf')
# drawing = svg2rlg(image_path)
# renderPDF.draw(drawing, my_canvas, 0, 40)
# my_canvas.drawString(50, 30, 'My SVG Image')
# my_canvas.save()

#
# save_dir = 'teamnamen_logo/'
# teams = read_teamnames('teamnamen sorted.txt')
# for t in teams:
#     dwg = svgwrite.Drawing(save_dir + t + '.svg', (200, 200), debug=True)
#     paragraph = dwg.add(dwg.g(font_size=14, style='font-family:TESLAFONT;'))
#     paragraph.add(dwg.text(t.upper(), (10, 20)))
#     dwg.save()
