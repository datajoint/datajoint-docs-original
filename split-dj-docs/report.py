#!/usr/local/bin/python3

import os
import re
import pandas as pd

pd.options.display.width = 120
pd.options.display.precision = 1

pattern = re.compile(r'\.\.\s+progress:\s+(?P<hours>\d*\.?\d*)\s*(?P<percent>\d+\.?\d*)%\s*(?P<author>\w+)\s*(?P<comment>.*)?$')

def filegen(path):
    for root, _, files in os.walk(path):
        for file in sorted(files):
            if file.endswith('.rst'):
                fullfile = os.path.join(root, file)
                with open(fullfile, 'rt') as f:
                    match = pattern.match(f.readline())
                    if match is None:
                        raise ValueError('File {file} has invalid progress report'.format(file=fullfile))
                    yield dict(match.groupdict(), section=root[len(path)+1:], file=file)

data = pd.DataFrame(filegen('./contents'))
data['hours'] = data['hours'].astype(float)
data['percent'] = data['percent'].astype(float)
data['done'] = data['hours']*data['percent']/100
data['remaining'] = data['hours']-data['done']

with open('./report.txt', 'wt') as f:

    print('\n'.join(str(data[['done','remaining']].sum()).split('\n')[:-1]), '\n\n', file=f)

    print(data.groupby('section')['author','done','remaining'].sum().sort_values(
        by='remaining', ascending=False),'\n\n', file=f)

    print(data.groupby('author')['author','done', 'remaining'].sum().sort_values(
        by='remaining', ascending=False), '\n\n', file=f)

    print(data[['author','section','file','done','remaining']].sort_values(
        by=['author', 'remaining'], ascending=[True, False]), file=f)
