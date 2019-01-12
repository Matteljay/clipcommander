#!/usr/bin/env python3
# to install directly, invoke via pip: sudo pip3 install .
# packages for PyPI.org: ./setup.py sdist bdist_wheel && twine upload dist/*

import setuptools
import os, sys, re
from pathlib import Path
mainscript = 'clipcommander.py'

resources = []
for fil in (f for f in Path('data').rglob('*') if f.is_file()):
    resources.append((str('share' / fil.parent.relative_to('data')), [str(fil)]))
with open('requirements.txt') as fh:
    required = fh.read().strip().splitlines()
with open('README.md', 'r') as fh:
    long_description = fh.read()
with open(mainscript) as fh:
    for line in fh:
        out = re.search(r'version = \u0027(.+?)\u0027$', line)
        if out:
            extracted_version = out.group(1)
            break
    try: extracted_version
    except NameError:
        print('ERROR: Could not extract version from ' + mainscript, file=sys.stderr)
        sys.exit(1)

setuptools.setup(
    name = 'clipcommander',
    version = extracted_version,
    author = 'Matteljay',
    author_email = 'matteljay@pm.me',
    description = 'Clipboard selection monitor YouTube-dl GUI front-end',
    long_description = long_description,
    long_description_content_type = 'text/markdown',
    url = 'https://github.com/Matteljay/clipcommander',
    scripts = [ mainscript ],
    install_requires = required,
    packages = setuptools.find_packages(),
    classifiers = [
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    data_files = resources,
)

# End of file




