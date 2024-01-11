import numpy as np 
from lhereader import LHEReader

reader = LHEReader('/grid_mnt/data__data.polcms/cms/spallacci/CMSSW_11_3_4/src/EFT2Obs/test-WG-LO/events_2.lhe')

bins = np.linspace(130, 1050, 21)
cw = [0, 0.01, 0.03, 0.05]
h = [[0] * (len(bins) - 1) for _ in range(4)]

for iev, event in enumerate(reader):
    phot = filter(lambda x: abs(x.pdgid) == 22, event.particles)
    coeff = np.dot(np.linalg.inv(np.array([[0.005, 0.000025], 
                    [0.01, 0.0001]])) ,np.array([[event.weights[1]/event.weights[0]-1],
                                                    [event.weights[2]/event.weights[0]-1]]))
    
    for x in phot:
        
        for n in range(len(cw)):
            
            mu = float(1 + coeff[0]*cw[n] + coeff[1]*cw[n]**2)
            bin_index = np.digitize(x.p4().pt, bins) - 1

            if 0 <= bin_index < len(h[n]):
                h[n][bin_index] += mu
               



