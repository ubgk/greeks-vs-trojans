import re

file = open("kill_list.txt", "r")

pat = r'^((\S+ )?(\S+)) \((A|T)\) kills (\S+) \((A|T)\)'

characters = dict()

victims = dict()
killers = set()

kills = dict()

pat = re.compile(pat)

matching_lines = []

for line in file:
    match = pat.match(line)

    if match:
        matching_lines.append(line)
        killer, _, _, killer_side, killed, killed_side = match.groups()

        killers.add(killer)

        victims[killed] = killer

        if killer not in characters:
            characters[killer] = killer_side

        if killed not in characters:
            characters[killed] = killed_side

        if killer not in kills:
            kills[killer] = [killed]
        else:
            kills[killer].append(killed)


def get_uri(name):
    return f"http://www.semanticweb.org/thomas/ontologies/2022/10/trojan-war#{name}"
