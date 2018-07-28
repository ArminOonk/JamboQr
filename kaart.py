import json
import svgwrite
import pyqrcode


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
    dwg = svgwrite.Drawing('teamnamen_logo/' + team + '.svg', (1000, 1000), debug=True)
    paragraph = dwg.add(dwg.g(font_size=72, style='font-family:TESLAFONT;'))
    paragraph.add(dwg.text(team, (250, 100), text_anchor='middle'))
    paragraph.add(dwg.text(team, (750, 100), text_anchor='middle'))
    paragraph.add(dwg.text(team, (250, 600), text_anchor='middle'))
    paragraph.add(dwg.text(team, (750, 600), text_anchor='middle'))

    lines = dwg.add(dwg.g(stroke_width=2, stroke='black', fill='none'))
    lines.add(dwg.line(start=(0, 500), end=(1000, 500)))
    lines.add(dwg.line(start=(500, 0), end=(500, 1000)))

    # QR code
    qr_name = 'STOP'
    qr = pyqrcode.create('jambo:' + qr_name + ':' + question['ans'], error='H')
    qr_svg(dwg, qr.text(), 100, 100, 10)

    # Question
    question_text = dwg.add(dwg.g(font_size=24, style='font-family:TESLAFONT;'))
    question_text.add(dwg.text('Vraag: ', (750, 200), text_anchor='middle'))
    question_text.add(dwg.text(question['q'], (750, 300), text_anchor='middle'))

    # Answer
    ans_text = dwg.add(dwg.g(font_size=24, style='font-family:TESLAFONT;'))
    ans_text.add(dwg.text('A: ' + question['a'], (100, 750)))
    ans_text.add(dwg.text('B: ' + question['b'], (100, 800)))
    ans_text.add(dwg.text('C: ' + question['c'], (100, 850)))
    ans_text.add(dwg.text('D: ' + question['d'], (100, 900)))

    # Color
    color = {'a': 'Rood', 'b': 'Groen', 'c': 'Geel', 'd': 'Oranje'}
    color_text = dwg.add(dwg.g(font_size=72, style='font-family:TESLAFONT;'))
    color_text.add(dwg.text('Kleur: ' + color[question['ans']], (750, 750), text_anchor='middle'))

    dwg.save()


with open('question.txt', 'r') as f:
    questions = json.load(f)

teams = read_teamnames('teamnamen sorted.txt')
page_number = 0
for t in teams:
    create_page(t.upper(), questions[page_number % len(questions)])
    page_number += 1

# save_dir = 'teamnamen_logo/'
# teams = read_teamnames('teamnamen sorted.txt')
# for t in teams:
#     dwg = svgwrite.Drawing(save_dir + t + '.svg', (200, 200), debug=True)
#     paragraph = dwg.add(dwg.g(font_size=14, style='font-family:TESLAFONT;'))
#     paragraph.add(dwg.text(t.upper(), (10, 20)))
#     dwg.save()

