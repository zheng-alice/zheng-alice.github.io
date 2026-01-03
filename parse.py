import re
from datetime import date
import bibtexparser
from bibtexparser.bparser import BibTexParser
from bibtexparser.customization import *
from jinja2 import Environment, FileSystemLoader

def customizations(record):

    # Render names as First Last
    for field in ['author', 'editor']:
        if field not in record: continue
        names = list()
        for name in re.split(r'\ and\ ', record[field].replace('\n', ' '), flags=re.IGNORECASE):
            split = splitname(name.strip())
            name = ''
            for part in ['first', 'von', 'last', 'jr']:
                if not split[part]: continue
                name = name + (' ' if name else '') + ' '.join(split[part])
            names.append(name)
        record[field] = names

    # Attempt to render math as unicode
    record = convert_to_unicode(record)
    record['title'] = record['title'].replace('$', '')

    # Replace double hyphens
    if 'pages' in record:
        record['pages'] = record['pages'].replace('--', '–')

    print(record)
    return record

parser = BibTexParser()
parser.customization = customizations
with open('publications.bib', 'r') as f:
    lib = bibtexparser.load(f, parser=parser)

env = Environment(loader=FileSystemLoader('templates'))
html = env.get_template('index.html').render({
    'name': 'Alice Zheng',
    'lib': lib.entries,
    'icons': [
        ["Google Scholar", 'scholar', "https://scholar.google.com/citations?user=xQbR0vcAAAAJ"],
        ["arXiv", 'arxiv', "https://arxiv.org/a/zheng_a_1.html"],
        ["ORCID", 'orcid', "https://orcid.org/0009-0009-9470-4941"]
    ],
    'date': date.today().strftime("%B %d, %Y")
})
with open('site/index.html', 'w') as fout:
    fout.write(html)
