# Der setgenerator erstellt .ini Dateien mit den Processparametern für
# die automatische Verarbeitung von Bildpaaren. Aus den definierten
# Parametern wird jede darause mögliche Kombination zu einem set zusammengestellt
# und als .ini Datei gespeichert.
#
# Strings in Ntup immer als Liste verkapseln: ['Text'], weil 'Text' sonst zerlegt (=Liste von Chars)
# Leere Einträge in Ntup immer so definieren: [None]

import collections
import itertools
import datetime
import configparser


# Extraktor Konfiguration definieren

Ntup = collections.namedtuple('ExtractorParams', 'type threshold specialflag rareAttribute')
parameters = [
    Ntup(type=['BRISK'], threshold=[10, 20, 50, 100, 500], specialflag=[True, False], rareAttribute=['nix']),
    Ntup(type=['ORB'], threshold=[10, 20, 50, 100, 300], specialflag=[True], rareAttribute=['dense', 'sparse'])
]
all_extractor_names = Ntup._fields
all_extractor_defs = list()
for item in parameters:
    tmplist = list(itertools.product(*item))
    all_extractor_defs.extend(tmplist)



# Deskriptor Konfiguration definieren

Ntup = collections.namedtuple('DescriptorParams', 'type param1 param2')
parameters = [
    Ntup(type=['SURF'], param1=[0, 1, 5], param2=[None, True, False]),
    Ntup(type=['FREAK'], param1=[10, 11, 55, 450], param2=[None])
]
all_descriptor_names = Ntup._fields
all_descriptor_defs = list()
for item in parameters:
    tmplist = list(itertools.product(*item))
    all_descriptor_defs.extend(tmplist)



# Alle Prozess Schritte kombinieren
all_combinations = itertools.product(all_extractor_defs, all_descriptor_defs)
masterlist = list(all_combinations)
datestring = datetime.datetime.now().strftime("%Y-%m-%d")

#Sectioncontrol bauen
sectionnames = ('detector', 'extractor')
fieldnames = (all_extractor_names, all_descriptor_names)
sectionids = tuple(range(len(sectionnames)))
sectioncontrol = list(zip(sectionids, sectionnames, fieldnames))


# Outputfile schreiben
configfile_basename = "tmp/cfg-test-" + datestring
filecounter = 0
for oneconfig in masterlist:
    filecounter += 1
    configfile_name = configfile_basename + str(filecounter).zfill(8) + '.ini'
    print(configfile_name)
    cfgfile = open(configfile_name, 'w')
    Config = configparser.ConfigParser()

# HEADER
    Config.add_section('File')
    Config.set('File', 'filename', configfile_name)

# SECTIONS
    for section in sectioncontrol:
        # ONE SECTION
        sectionid, sectionname, fieldnames = section
        Config.add_section(sectionname)
        for item in list(zip(fieldnames, oneconfig[sectionid])):
            fname, val = item
            Config.set(sectionname, str(fname), str(val))

    Config.write(cfgfile)
    cfgfile.close()
