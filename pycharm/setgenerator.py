# Der setgenerator erstellt .ini Dateien mit den Processparametern für
# die automatische Verarbeitung von Bildpaaren. Aus den definierten
# Parametern wird jede mögliche Kombination zu einem set zusammengestellt
# und als .ini Datei gespeichert.

import collections
import itertools




# Extraktor Konfiguration definieren
Def1 = collections.namedtuple('ExtractorParams', 'type threshold specialflag rareAttribube')
def1 = [
    Def1(type=['BRISK'], threshold=[10, 20, 50, 100, 500], specialflag=[True, False], rareAttribube=['nix']),
    Def1(type=['ORB'], threshold=[10, 20, 50, 100, 300], specialflag=[True], rareAttribube=['dense', 'sparse'])
]
all_extractor_names = Def1._fields
all_extractor_defs = list()
for item in def1:
    tmplist = list(itertools.product(*item))
    all_extractor_defs.extend(tmplist)



# Deskriptor Konfiguration definieren
def2 = collections.namedtuple('DescriptorParams', 'type param1 param2')
descriptordef = [
    def2(type=['BRISK'], param1=[0, 1, 5], param2=[]),
    def2(type=['FREAK'], param1=[10, 11, 55], param2=[])
]
all_descriptor_names = def2._fields
all_descriptor_defs = list()
for item in descriptordef:
    tmplist = list(itertools.product(*item))
    all_extractor_defs.extend(tmplist)



#

for fld in et1._fields:
    attrib = getattr(et1, fld)
    print(str(fld) + ": " + str(attrib))
    if type(attrib) is list:
        for item in attrib:
            print(' ---> ' + str(item))



extractor = []
extractor.append(['ORB', 100, 200, 300, 500])




for detail in extractor[0]:
    print(detail)

