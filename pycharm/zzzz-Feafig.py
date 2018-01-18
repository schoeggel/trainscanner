import util

camcal = util.loadconfig('cfg/cameracalib.mat')
conf = util.loadconfig('cfg/process/process1.mat', 'process')
c = conf.__dict__
util.saveconfig('out/matwritetest.mat', c)
