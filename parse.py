# Fill in details in site template (citations, date, etc.)
import os
import re
import subprocess
from collections import defaultdict
from datetime import date, datetime
import xml.etree.ElementTree as ET
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

uname = 'zheng-alice'
base = f'https://{uname}.github.io'
now = datetime.now().astimezone().isoformat(timespec='seconds')
env = Environment(loader=FileSystemLoader('templates'),extensions=['jinja2.ext.loopcontrols'])
html = env.get_template('index.html').render({
    'name': 'Alice Zheng',
    'base': base,
    'source': f'https://github.com/{uname}/{uname}.github.io',
    'lib': lib.entries,
    'icons': [
        ["Google Scholar", 'scholar', "https://scholar.google.com/citations?user=xQbR0vcAAAAJ"],
        ["arXiv", 'arxiv', "https://arxiv.org/a/zheng_a_1.html"],
        ["ORCID", 'orcid', "https://orcid.org/0009-0009-9470-4941"]
    ],
    'datetime_iso': now,
    'date': date.today().strftime("%B %d, %Y")
})
with open('site/index.html', 'w') as fout:
    fout.write(html)

# Generate sitemap
sitemap = ET.Element('urlset', xmlns="http://www.sitemaps.org/schemas/sitemap/0.9")
sitemap.attrib['xmlns:image'] = "http://www.google.com/schemas/sitemap-image/1.1"
def add_url(loc, mod, freq, pri):
    url = ET.SubElement(sitemap, 'url')
    ET.SubElement(url, 'loc').text = loc
    if mod: ET.SubElement(url, 'lastmod').text = mod
    ET.SubElement(url, 'changefreq').text = freq
    ET.SubElement(url, 'priority').text = pri
    return url

main = add_url(base, now, 'monthly', '1.0')
imgs = defaultdict(int)
imgname = re.compile(r"^(.*?)(\d+)\.webp$")
for file in os.listdir(f'site/images'):
    name, val = imgname.match(file).groups()
    imgs[name] = max(imgs[name], int(val))
for name, val in imgs.items():
    ET.SubElement(ET.SubElement(main, 'image:image'), 'image:loc').text = f'{base}/images/{name}{val}.webp'
for loc in ['talks', 'posters']:
    for file in os.listdir(f'site/{loc}'):
        cmd = ['git', 'log', '-1', '--format=%aI', f'site/{loc}/{file}']
        mod = subprocess.run(cmd, check=True, text=True, capture_output=True).stdout.strip()
        add_url(f'{base}/{loc}/{file}', mod, 'never', '0.4')

tree = ET.ElementTree(sitemap)
ET.indent(tree, space="\t", level=0)
ET.ElementTree(sitemap).write(f'site/sitemap.xml', encoding='UTF-8', xml_declaration=True)
