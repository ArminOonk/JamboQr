import json
import svgwrite


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


save_dir = 'teamnamen_logo/'
teams = read_teamnames('teamnamen sorted.txt')
for t in teams:
    dwg = svgwrite.Drawing(save_dir + t + '.svg', (200, 200), debug=True)
    paragraph = dwg.add(dwg.g(font_size=14, style='font-family:TESLAFONT;'))
    paragraph.add(dwg.text(t.upper(), (10, 20)))
    dwg.save()

# questions = []
# d = dict()
# d['q'] = 'Wie is de teamleider van TEAT?'
# d['a'] = 'Donald duck'
# d['b'] = 'Michiel'
# d['c'] = 'Jan Smit'
# d['d'] = 'Wybo'
# d['ans'] = 'b'
# questions.append(d)
#
# e = dict()
# e['q'] = 'Wie is de teamleider van Aqua?'
# e['a'] = 'Donald duck'
# e['b'] = 'Pien'
# e['c'] = 'Jan Smit'
# e['d'] = 'Neptunes'
# e['ans'] = 'd'
# questions.append(e)
#
# with open('question.txt', 'w') as f:
#     f.write(json.dumps(questions, sort_keys=True, indent=4))
