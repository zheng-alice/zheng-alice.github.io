# Subset font files to contain precisely the used characters
import codecs
import os
import re
import shutil
import subprocess

'''Doing it this way is admittedly pretty hacky.
I tried a bunch of existing tools, but they all seem to differ slightly from
the intended functionality. Instead, I use one to search for used characters
and another to subset, using this script to pass intermediate data.'''

# 1. subfont: Search website and generate lists of used characters
shutil.copytree("templates/fonts", "site/fonts", dirs_exist_ok=True)
cmd = ['subfont', '--debug', '--dry-run', 'site/index.html']
out = subprocess.run(cmd, check=True, text=True, stdout=subprocess.PIPE).stdout
shutil.rmtree("site/fonts")

# 2. pyftsubset: Create subsets of font files
os.mkdir("site/fonts")
fonts = re.findall(r"src: 'url\(fonts\/(.*)\.woff2\)',", out)
texts = re.findall(r"text: (.*),", out)
for font, t in zip(fonts, texts):
    text = re.sub(r"\\(.)", lambda c: codecs.decode('\\'+c.group(1), 'unicode_escape'), t[1:-1])
    uni = ','.join(map(lambda c: f'{ord(c):X}', text))
    print(f"{font}:{text}\n{uni}")
    cmd = ['pyftsubset', f'templates/fonts/{font}.woff2', '--verbose', '--flavor=woff2', f'--output-file=site/fonts/{font}.woff2', f'--unicodes={uni}']
    try:
        res = subprocess.run(cmd, check=True, text=True, capture_output=True)
    except subprocess.CalledProcessError as e: res = e
    finally:
        print(res.stderr)
