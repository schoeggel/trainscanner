# Der setgenerator erstellt .ini Dateien mit den Processparametern für
# die automatische Verarbeitung von Bildpaaren. Aus den definierten
# Parametern wird jede darause mögliche Kombination zu einem set zusammengestellt
# und als .ini Datei gespeichert.
#
# Strings in Ntup immer als Liste verkapseln: ['Text'], weil 'Text' sonst zerlegt (=Liste von Chars)
# Leere Einträge in Ntup immer so definieren: [None]
# Die Bezeichner sind case insensitiv. type: 'BRISK' ist gleich wie TYPE: 'BRISK'
# Die Werte sind case sensitiv. type: 'BRISK' != type: 'brisk'

# todo: eventuell kann umgeschrieben werden ohne named tuple, so dass nur noch die wirklich benötigten paramter angegeben werden müssen



import collections
import itertools
import datetime
import configparser
from random import shuffle


def rejectConfig(configList):
    # Liefert true, wenn die Konfigurations verworfen werden soll.
    # Bspw. wenn Desktriptor und Extraktor Typen gleich sind, aber ihre Parameter nicht.
    # Die Typen sind in den Arrays 0 und 1 an erster Stelle gespeichert. [0][0] und [1][0] sind die Typen
    # None-Typen kommen nicht bis hierher, keine Prüfung nötig

    # Die Typen sind unterschiedlich --> Keine Optimierung möglich
    if configList[0][0] != configList[1][0]:
        return False

    # Die Typen sind identisch --> Nur die komplett identische Variante behalten
    if configList[0] != configList[1]:
        return True

    return False



# Extraktor Konfiguration definieren, Leerschlag beachten!
Ntup = collections.namedtuple('something',
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

    Ntup(type=['FAST'],
         maxfeatures=[None],
         threshold=[10, 20, 60],
         levels=[None],
         octaves=[None],
         octaveLayers=[None],
         scale=[0, 1, 2],  # FAST Type (5_8  / 7_12  / 9_16)
         fast_nonmaxSuppression=[0, 1],  # default true
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

    Ntup(type=['FREAK'],
         maxfeatures=[None],
         threshold=[None],
         levels=[None],
         octaves=[2, 4, 6],
         octaveLayers=[None],
         scale=[22.0, 41.0, 67.0],
         fast_nonmaxSuppression=[None],
         mser_delta=[None],
         orb_WTAK=[None],
         extended=[None],
         upright=[None],
         freak_scalenormalized=[None],
         futureArgument1=[None]),

    Ntup(type=["LATCH"],
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


#Filter
Ntup = collections.namedtuple('something',
                              'maxFeatures '
                              'reproMaxDistance')

parameters = [
    Ntup(maxFeatures=[50000],
         reproMaxDistance=[3, 9])]

all_filter_names = Ntup._fields
all_filter_defs = list()
for item in parameters:
    tmplist = list(itertools.product(*item))
    all_filter_defs.extend(tmplist)


# 3d
Ntup = collections.namedtuple('something',
                              'MatrixF '
                              'param1 '
                              'param2')

parameters = [
    Ntup(MatrixF=['RANSAC'],            # use RANSAC to estimate F Matrix
         param1=[None],
         param2=[None]),

    Ntup(MatrixF=['CALIBRATION'],       # use F stored in calibration File
         param1=[None],
         param2=[None])
]

all_3d_names = Ntup._fields
all_3d_defs = list()
for item in parameters:
    tmplist = list(itertools.product(*item))
    all_3d_defs.extend(tmplist)





# Alle Prozess Schritte kombinieren
all_combinations = itertools.product(all_extractor_defs, all_descriptor_defs, all_filter_defs, all_3d_defs)
masterlist = list(all_combinations)
datestring = datetime.datetime.now().strftime("%Y-%m-%d")

#Sectioncontrol bauen
#Die .ini Datei ist in sections unterteilt.
sectionnames = ('detector', 'extractor', 'Filter', '3d')
fieldnames = (all_extractor_names, all_descriptor_names, all_filter_names, all_3d_names)
sectionids = tuple(range(len(sectionnames)))
sectioncontrol = list(zip(sectionids, sectionnames, fieldnames))


# Outputfile schreiben
verb = True         # Zeigt jeden Datainamen in der Console an.
dryrun = False       # ohne Dateien zu schreiben.
configfile_dir = "tmp/" # "cfg/ini-batch1/"
configfile_basename = "cfg-test-" + datestring
configfile_root = configfile_dir + configfile_basename
filecounterWritten = 0
filecounterSkipped = 0
shuffle(masterlist)     # Fehler werden früher erkannt in der Batchverarbeitung
for oneconfig in masterlist:
    if rejectConfig(oneconfig):
        if verb:
            print('ExtractorType=DescriptorType while using different paramters. -->  No .ini File written.')
        filecounterSkipped += 1
        continue

    filecounterWritten += 1
    configfile_fullpath = configfile_root + str(filecounterWritten).zfill(8) + '.ini'
    if verb:
        status = str(+ filecounterWritten) + "/" + str(filecounterSkipped) + "/" + str(filecounterSkipped+filecounterWritten)
        print('written/skipped/total: ' + status + " | " + configfile_fullpath)
    if not dryrun:
        cfgfile = open(configfile_fullpath, 'w')
        Config = configparser.ConfigParser()

    # HEADER
        Config.add_section('file')
        Config.set('file', 'configfile', configfile_fullpath)
        Config.set('file', 'name', configfile_basename + str(filecounterWritten).zfill(8))

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

status = str(+ filecounterWritten) + "/" + str(filecounterSkipped) + "/" + str(filecounterSkipped + filecounterWritten)
print('\nReport:\n------\n')
print('written\t' + str(filecounterWritten))
print('skipped\t' + str(filecounterSkipped))
print('total  \t' + str(filecounterWritten+filecounterSkipped))
