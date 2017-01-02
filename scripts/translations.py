# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import io
import os
import csv
import collections
import polib
import click

# from here
import compat


SCRIPTS_DIR = os.path.dirname(__file__)
BASE_DIR = os.path.dirname(SCRIPTS_DIR)
TRANS_DIR = os.path.join(BASE_DIR, 'trans')

DATA_FILENAME = 'data.csv'
DATA = os.path.join(BASE_DIR, DATA_FILENAME)
ENPO = os.path.join(TRANS_DIR, 'en.po')
HEPO = os.path.join(TRANS_DIR, 'he.po')
ARPO = os.path.join(TRANS_DIR, 'ar.po')
RUPO = os.path.join(TRANS_DIR, 'ru.po')
AMPO = os.path.join(TRANS_DIR, 'am.po')
FRPO = os.path.join(TRANS_DIR, 'fr.po')

metadata = {
    'Project-Id-Version': '1.0',
    'Report-Msgid-Bugs-To': 'paulywalsh@gmail.com',
    'POT-Creation-Date': '2015-04-04 00:00+0200',
    'PO-Revision-Date': '20015-04-04 00:01+0200',
    'Last-Translator': 'Paul Walsh <paulywalsh@gmail.com>',
    'Language-Team': 'English <paulywalsh@gmail.com>',
    'MIME-Version': '1.0',
    'Content-Type': 'text/plain; charset=utf-8',
    'Content-Transfer-Encoding': '8bit',
}

enpo = polib.POFile()
hepo = polib.POFile()
arpo = polib.POFile()
rupo = polib.POFile()
ampo = polib.POFile()
frpo = polib.POFile()
_pos = enpo, hepo, arpo, rupo, ampo, frpo
for _po in _pos:
    _po.metadata = metadata

languages = [
    {
        'id': 'en',
        'file': ENPO,
        'po': enpo
    },
    {
        'id': 'he',
        'file': HEPO,
        'po': hepo
    },
    {
        'id': 'ar',
        'file': ARPO,
        'po': arpo
    },
    {
        'id': 'ru',
        'file': RUPO,
        'po': rupo
    },
    {
        'id': 'am',
        'file': AMPO,
        'po': ampo
    },
    {
        'id': 'fr',
        'file': FRPO,
        'po': frpo
    }
]

def run():

    lookup = collections.OrderedDict()

    with io.open(DATA, mode='r+t', encoding='utf-8') as stream:
        reader = compat.csv_reader(stream)
        headers = next(reader)

        for index, row in enumerate(reader):

            # po format doesn't like 0 as a line number
            index += 1

            mapping = dict(zip(headers, row))

            if mapping.get('name'):

                msgid = mapping['name']

                if msgid in lookup:
                    lookup[msgid]['occurences'].append((DATA_FILENAME, index))
                else:
                    lookup[msgid] = {'occurences': [], 'translations': {}}
                    lookup[msgid]['occurences'].append((DATA_FILENAME, index))

                lookup[msgid]['translations']['en'] = mapping['name']
                lookup[msgid]['translations']['he'] = mapping['name@he']
                lookup[msgid]['translations']['ar'] = mapping['name@ar']
                lookup[msgid]['translations']['ru'] = mapping['name@ru']
                lookup[msgid]['translations']['am'] = mapping['name@am']
                lookup[msgid]['translations']['fr'] = mapping['name@fr']

            if mapping.get('description'):

                msgid = mapping['description']

                if msgid in lookup:
                    lookup[msgid]['occurences'].append((DATA_FILENAME, index))
                else:
                    lookup[msgid] = {'occurences': [], 'translations': {}}
                    lookup[msgid]['occurences'].append((DATA_FILENAME, index))

                lookup[msgid]['translations']['en'] = mapping['description']
                lookup[msgid]['translations']['he'] = mapping['description@he']
                lookup[msgid]['translations']['ar'] = mapping['description@ar']
                lookup[msgid]['translations']['ru'] = mapping['description@ru']
                lookup[msgid]['translations']['am'] = mapping['description@am']
                lookup[msgid]['translations']['fr'] = mapping['description@fr']

    for msgid, data in lookup.items():

        for lang in languages:
            entry = polib.POEntry(
                msgid=msgid,
                msgstr=data['translations'][lang['id']],
                occurrences=data['occurences']
            )
            lang['po'].append(entry)

    for lang in languages:
        lang['po'].save(lang['file'])
