from xml.dom import minidom

import utils

ont_name = "trojan-war"
dom = minidom.parse(f'{ont_name}.owl')

named_individuals = dom.getElementsByTagName('owl:NamedIndividual')
existing_individuals = dict()


def create_individual(name, dom):
    side = utils.characters[name]
    side = {'T': 'Trojan', 'A': 'Greek'}[side]

    ind_elem = dom.createElement('owl:NamedIndividual')
    ind_elem.setAttribute("rdf:about", utils.get_uri(name))

    automated_elem = dom.createElement('rdf:type')
    automated_elem.setAttribute("rdf:resource", utils.get_uri("Automated"))
    ind_elem.appendChild(automated_elem)

    side_elem = dom.createElement('rdf:type')
    side_elem.setAttribute("rdf:resource", utils.get_uri(side))
    ind_elem.appendChild(side_elem)

    comment_elem = dom.createComment(" Automated Entry ")
    dom.firstChild.appendChild(comment_elem)

    comment_elem = dom.createComment(" " + utils.get_uri(name) + " ")
    dom.firstChild.appendChild(comment_elem)

    dom.firstChild.appendChild(ind_elem)

    return ind_elem


for n_ind in named_individuals:
    name = n_ind.getAttribute("rdf:about").split('#')[1]

    existing_individuals[name] = n_ind

for vict, killer in utils.victims.items():
    if vict in existing_individuals:
        vict_elem = existing_individuals[vict]
    else:
        vict_elem = create_individual(vict, dom)
        pass

    if killer in existing_individuals:
        killer_elem = existing_individuals[killer]
    else:
        killer_elem = create_individual(killer, dom)

    killer_ref = killer_elem.getAttribute("rdf:about")

    killed_by_elem = dom.createElement("isKilledBy")
    killed_by_elem.setAttribute("rdf:resource", killer_ref)

    vict_elem.appendChild(killed_by_elem)


# dom.getElementsByTagName("owl:Ontology")[0].setAttribute("rdf:about", f"{ont_name}-auto")

new_ontology = dom.toprettyxml()

with open(f"{ont_name}.owl", "w") as f:
    f.write(new_ontology)
