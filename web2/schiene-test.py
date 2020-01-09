import schiene

connections = []
connections.append(('Stuttgart Universität', 'Stuttgart Hbf'))
connections.append(('Stuttgart Hbf', 'Mannheim Hbf'))
# connections.append(('Mannheim Friedrichsfeld-Süd', 'Mannheim Hbf'))
# connections.append(('Mannheim Hbf', 'Stuttgart Hbf'))

s = schiene.Schiene()
for c in connections:
    print('{} - {}'.format(*c))
    res = s.connections(*c)
    for v in res:
        delay = 0
        if 'delay' in v:
            delay = v['delay']['delay_departure']
        print('    Abfahrt: {} | +{}'.format(v['departure'], delay))
