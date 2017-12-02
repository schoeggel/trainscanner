# Verschiedene Hilfsfunktionen
import scipy.io.matlab
from ruamel.yaml import YAML
import configparser


def saveconfig(filename, dic, structname='python'):
    if '.mat' in filename:
        ___saveconfigmat(filename, dic, structname)




def loadconfig(filename, structname='paramStruct'):
    if '.mat' in filename:
        return ___loadconfigmat(filename, structname)
    if '.yaml' in filename or '.yml' in filename:
        return ___loadconfigyaml(filename)
    if '.ini' in filename:
        return ___loadconfigini(filename)


# Lädt ein .mat File und liefert das angegebene Struct zurück.
# Es kann auf dem Returnobjekt direkt mit den Strukturnamen gearbeitet werden:
# obj.CameraData1.ImageSize  etc...
# siehe https://docs.scipy.org/doc/scipy/reference/tutorial/io.html
def ___loadconfigmat(filename, structname='paramStruct'):
    cfg = scipy.io.loadmat(filename, struct_as_record=False, squeeze_me=True)
    return cfg[structname]



# Lädt ein YAML. Auf dem Return Objekt muss etwas umständlicher auf die Daten zugegriffen werden:
# obj['CameraData1'
def ___loadconfigyaml(filename):
    with open(filename, 'r') as ymlfile:
        yaml = YAML(typ='safe')  # default, if not specfied, is 'rt' (round-trip)
        yaml.load(filename)
        return pyaml.load(ymlfile)


# TODO: Fertigstellen !
# Lädt ein ini. Auf dem Return Objekt muss etwas umständlicher auf die Daten zugegriffen werden:
# obj['CameraData1']
# NOCH NICHT GETESTET / FERTIG !!!
def ___loadconfigini(filename):
    cfg = configparser.ConfigParser()
    cfg.read(filename)
    cfg.sections()
    return cfg


def ___saveconfigmat(filename, dic, structname):
    scipy.io.savemat(filename, dic, False)





# gibt die eine option aus einem configparserobject zurück
# in der Form des bestgeeignetsten Datentyps. Int vor Float vor None vor String
class IniTypehandler:
    def __init__(self, configparserobject):
        self.cp = configparserobject

    def get(self, option):
        if option is None:
            raise Exception("expecting String as arg 1, received None")

        #Lese Option:
        try:
            content = self.cp[option]
        except:
            raise Exception("unknown error accessing option from configparser object")


        # Try to convert to int
        try:
            return int(content)
        except:
            pass

        # Try to convert to float
        try:
            return float(content)
        except:
            pass

        # Try to convert to string
        try:
            if content.lower() == "none":
                return
            else:
                return str(content)
        except:
            raise Exception("could not convert content from configparser object")
