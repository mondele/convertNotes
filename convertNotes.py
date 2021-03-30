#!/usr/bin/env python3
#convertNotes.py
#version 0.1

import os
from collections import defaultdict
import fileinput
import glob
import string, sys
import ast

siglalivro = 'deu'
nomedoLivro = 'Deuteronomy'
basepath = 'E:\\MAST2020\\deut_notas\\pt-br_deu_tn_3'

projeto = 'pt-br_{0}_tn'.format(siglalivro)

arquivos = defaultdict(list)
conteudo = []
for entry in os.listdir(basepath):
    if (not os.path.isfile(os.path.join(basepath, entry))) and (entry not in {'.git', 'front'}):
        gl = glob.glob(basepath + "\\" + entry + "\\" + ".md")
        openhook = fileinput.hook_encoded("utf-8", "surrogateescape")
        finput = fileinput.input(gl, openhook=openhook)
        for line in finput:
            if "intro.md" not in finput.filename():
                conteudo.append(line)
        finput.close()
print ('Number of lines imported: ',len(conteudo))

def limpeza_inicial(texto):
    return texto.replace('\n','').replace('\r','').replace('<o:p style="background-color: rgb (255, 255, 255);">','').replace('&nbsp;',' ').replace(u'\xa0',' ').replace(u'\xa0T',' ').replace('<o:p>',' ').replace('</o:p>',' ').replace('"','\\"').replace('#####','').replace('\`','').replace('<u style="font-weight: bold;">','').replace('</u>','').replace('<u>','').replace('####','')

conteudolimpo = [ '{} |***| {}'.format(line, limpeza_inicial(line))
                for line in conteudo if (len(line) >= 4)]
conteudolimpo[0:5]

def list_referencia(texto):
    import re
    return [ '[[{0}]]'].format(i) for i in re.findall ('(?<=\[\[)([^]]+)(?=\]\])', texto, flags=0)]
    
referencias = []
for line in conteudolimpo:
    ref = list_referencia(line)
    if len(ref) > 0:
        referencias = referencias + ref
referencias.sort()

tiposref = {}
for item in set(referencias):
    tiposref[item] = referencias.count(item)

depara = '{' + ', '.join(['"{0}":"{1}"'.format(refnova, refnova.replace('rc://en/ta/man/translate/','').('-','_').replace('rc://en/tw/dict/bible/kt/','').replace('[','').replace(']','').replace('rc: // pt / ta / man / translate / ','').replace('rc://e n/ta/man/translate/',''))
    for refnova in set(referencias)] ) + '}'
depara = ast.literal_eval(depara)

