# Der setgenerator erstellt .ini Dateien mit den Processparametern für
# die automatische Verarbeitung von Bildpaaren. Aus den definierten
# Parametern wird jede darause mögliche Kombination zu einem set zusammengestellt
# und als .ini Datei gespeichert.
#
# Strings in Ntup immer als Liste verkapseln: ['Text'], weil 'Text' sonst zerlegt (=Liste von Chars)
# Leere Einträge in Ntup immer so definieren: [None]
# Die Bezeichner sind case insensitiv. type: 'BRISK' ist gleich wie TYPE: 'BRISK'
# Die Werte sind case sensitiv. type: 'BRISK' != type: 'brisk'
#todo: umschreiben, damit die detectoren und descriptoren im falle des gleichen typs
#todo: auch die gleichen paramter aufweisen. das würde die Kombinationen drastisch reduzieren.
#todo: eventuell kann umgeschrieben werden ohne named tuple, so dass nur noch die wirklich benötigten paramter angegeben werden müssen



import collections
import itertools
import datetime
import configparser


# Extraktor Konfiguration definieren
Ntup = collections.namedtuple('ExtractorParams',
                              'type '
                              'maxfeatures '                 # nfeatures – The maximum number of features to retain.
                              'threshold '
                              'levels '
                              'octaves '
                              'octaveLayers ' 
                              'scale '
                              'fast_nonmaxSuppression '
                              'mser_delta '                     
                              'orb_WTAK '   
                              'extended '
                              'upright '
                              'freak_scalenormalized '
                              'futureArgument1')
parameters = [
    Ntup(type=['BRISK'],
         threshold=[10, 20, 50, 100],           # default = 30
         octaves=[2, 3, 5],                     # default = 3
         scale=[0.66, 1.00, 1.66],              # default = 1.00
         maxfeatures=[None],
         levels=[None],
         octaveLayers=[None],
         fast_nonmaxSuppression=[None],
         mser_delta=[None],
         orb_WTAK=[None],
         extended=[None],
         upright=[None],
         freak_scalenormalized=[None],
         futureArgument1=[None]),

    Ntup(type=['ORB'],
         maxfeatures=[500, 5000, 10000],        # default = 500
         scale=[1.1, 1.2, 1.5],                 # default = 1.2
         levels=[4, 8, 16],                     # default = 8
         orb_WTAK=[2, 3, 4],                    # default = 2
         threshold=[None],
         octaves=[None],
         octaveLayers=[None],
         fast_nonmaxSuppression=[None],
         mser_delta=[None],
         extended=[None],
         upright=[None],
         freak_scalenormalized=[None],
         futureArgument1=[None]),

    Ntup(type=['SURF'],
         maxfeatures=[None],
         threshold=[300, 450, 1000],
         levels=[None],
         octaves=[4, 8, 12],                # default = 4
         octaveLayers=[2, 4],               # default = 2
         scale=[None],
         fast_nonmaxSuppression=[None],
         mser_delta=[None],
         orb_WTAK=[None],
         extended=[0, 1],
         upright=[0, 1],
         freak_scalenormalized=[None],
         futureArgument1=[None]),


    Ntup(type=[None],
         maxfeatures=[None],
         threshold=[None],
         levels=[None],
         octaves=[None],
         octaveLayers=[None],
         scale=[None],
         fast_nonmaxSuppression=[None],
         mser_delta=[None],
         orb_WTAK=[None],
         extended=[None],
         upright=[None],
         freak_scalenormalized=[None],
         futureArgument1=[None])
]
all_extractor_names = Ntup._fields
all_extractor_defs = list()
for item in parameters:
    tmplist = list(itertools.product(*item))
    all_extractor_defs.extend(tmplist)



# Deskriptor Konfiguration definieren
# Ntup bleibt gleich wie beim detector

parameters = [
    Ntup(type=['BRISK'],
         threshold=[10, 20, 50, 100],  # default = 30
         octaves=[2, 3, 5],  # default = 3
         scale=[0.66, 1.00, 1.66],  # default = 1.00
         maxfeatures=[None],
         levels=[None],
         octaveLayers=[None],
         fast_nonmaxSuppression=[None],
         mser_delta=[None],
         orb_WTAK=[None],
         extended=[None],
         upright=[None],
         freak_scalenormalized=[None],
         futureArgument1=[None]),

    Ntup(type=['ORB'],
         maxfeatures=[500, 5000, 10000],  # default = 500
         scale=[1.1, 1.2, 1.5],  # default = 1.2
         levels=[4, 8, 16],  # default = 8
         orb_WTAK=[2, 3, 4],  # default = 2
         threshold=[None],
         octaves=[None],
         octaveLayers=[None],
         fast_nonmaxSuppression=[None],
         mser_delta=[None],
         extended=[None],
         upright=[None],
         freak_scalenormalized=[None],
         futureArgument1=[None]),

    Ntup(type=['SURF'],
         maxfeatures=[None],
         threshold=[300, 450, 1000],
         levels=[None],
         octaves=[4, 8, 12],  # default = 4
         octaveLayers=[2, 4],  # default = 2
         scale=[None],
         fast_nonmaxSuppression=[None],
         mser_delta=[None],
         orb_WTAK=[None],
         extended=[0, 1],
         upright=[0, 1],
         freak_scalenormalized=[None],
         futureArgument1=[None]),

    Ntup(type=['FREAK'],
         maxfeatures=[None],
         threshold=[None],
         levels=[None],
         octaves=[None],
         octaveLayers=[None],
         scale=[None],
         fast_nonmaxSuppression=[None],
         mser_delta=[None],
         orb_WTAK=[None],
         extended=[None],
         upright=[None],
         freak_scalenormalized=[None],
         futureArgument1=[None]),

    Ntup(type=[None],
         maxfeatures=[None],
         threshold=[None],
         levels=[None],
         octaves=[None],
         octaveLayers=[None],
         scale=[None],
         fast_nonmaxSuppression=[None],
         mser_delta=[None],
         orb_WTAK=[None],
         extended=[None],
         upright=[None],
         freak_scalenormalized=[None],
         futureArgument1=[None])
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
    Config.add_section('file')
    Config.set('file', 'configfile', configfile_name)

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
