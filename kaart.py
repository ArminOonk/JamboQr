import json


teams = []
with open('teamnamen.txt', 'r') as f:
    for data in f.readlines():
        teams.append(data.strip())



print('Number of teams: ' + str(len(teams)))
print('Number of unique teams: ' + str(len(list(set(teams)))))
# print('Teams: ' + ' '.join(teams))

with open('teamnamen sorted.txt', 'w') as f:
    f.write('\n'.join(sorted(set(teams))))

questions = []
d = dict()
d['q'] = 'Wie is de teamleider van TEAT?'
d['a'] = 'Donald duck'
d['b'] = 'Michiel'
d['c'] = 'Jan Smit'
d['d'] = 'Wybo'
questions.append(d)

e = dict()
e['q'] = 'Wie is de teamleider van Aqua?'
e['a'] = 'Donald duck'
e['b'] = 'Neptunus'
e['c'] = 'Jan Smit'
e['d'] = 'Pien'
questions.append(e)

with open('question.txt', 'w') as f:
    f.write(json.dumps(questions, sort_keys=True, indent=4))
