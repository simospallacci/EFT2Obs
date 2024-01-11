import numpy as np 
from lhereader import LHEReader
import matplotlib.pyplot as plt
import mplhep as hep

reader = LHEReader('/grid_mnt/data__data.polcms/cms/spallacci/CMSSW_11_3_4/src/EFT2Obs/test-WG-LO/events_2.lhe')

#Photons transverse momentum
leptons_pt = []
leptons_eta = []
neutrino_pt = []
photons_pt = []
photons_eta = []

for iev, event in enumerate(reader):
    # Find photons
    print(event.weights[0])
    lept = filter(lambda x: abs(x.pdgid)== 11 or abs(x.pdgid)== 13 or abs(x.pdgid)== 15 or abs(x.pdgid)== 17 , event.particles)
    neutrino = filter(lambda x: abs(x.pdgid)== 12 or abs(x.pdgid)== 14 or abs(x.pdgid)== 16 or abs(x.pdgid)== 18 , event.particles)
    phot = filter(lambda x: abs(x.pdgid) == 22, event.particles)
    for x in lept:
        leptons_pt.append(x.p4().pt)
        leptons_eta.append(x.p4().eta)
    
    for x in neutrino:
        neutrino_pt.append(x.p4().pt)
    
    for x in phot:
        photons_pt.append(x.p4().pt)
        photons_eta.append(x.p4().eta)
    


plt.style.use(hep.style.CMS)

f2, axs2 = plt.subplots(figsize=(14, 7))
N = np.histogram(neutrino_pt, bins = np.linspace(min(neutrino_pt), max(neutrino_pt), 21))
n, bins2 = N
axs2.set_yscale('log')
hep.histplot(n, bins2, yerr=True, ax=axs2, histtype = 'fill')
plt.xlabel('Neutrinos pt')
plt.ylabel('Number of neutrinos per bin')
plt.title('Neutrinos pt')
plt.savefig('/grid_mnt/data__data.polcms/cms/spallacci/CMSSW_11_3_4/src/EFT2Obs/graphs/neutrino_pt_cw.png')

f, axs = plt.subplots(figsize=(14, 7))
H = np.histogram(leptons_pt, bins = np.linspace(min(leptons_pt), max(leptons_pt), 21))
h, bins = H
axs.set_yscale('log')
hep.histplot(h, bins, yerr=True, ax=axs, histtype = 'fill')
plt.xlabel('Leptons pt')
plt.ylabel('Number of leptons per bin')
plt.title('Leptons pt')
plt.savefig('/grid_mnt/data__data.polcms/cms/spallacci/CMSSW_11_3_4/src/EFT2Obs/graphs/leptons_pt_cw.png')

E = np.histogram(leptons_eta, bins = np.linspace(min(leptons_eta), max(leptons_eta), 21))
e, bins1 = E
f1, axs1 = plt.subplots(figsize=(14, 7))
axs1.set_yscale('log')
hep.histplot(e, bins1, yerr=True, ax=axs1, histtype = 'fill')
plt.xlabel('Leptons pseudorapidity')
plt.ylabel('Number of leptons per bin')
plt.title('Leptons pseudorapidity')
plt.savefig('/grid_mnt/data__data.polcms/cms/spallacci/CMSSW_11_3_4/src/EFT2Obs/graphs/leptons_eta_cw.png')

P = np.histogram(photons_pt, bins = np.linspace(min(photons_pt), max(photons_pt), 21))
p, bins3 = P
f3, axs3 = plt.subplots(figsize=(14, 7))
axs3.set_yscale('log')
hep.histplot(p, bins3, yerr=True, ax=axs3, histtype = 'fill')
plt.xlabel('Photons pt')
plt.ylabel('Number of photons per bin')
plt.title('Photons pt')
plt.savefig('/grid_mnt/data__data.polcms/cms/spallacci/CMSSW_11_3_4/src/EFT2Obs/graphs/photons_pt_cw.png')

P1 = np.histogram(photons_eta, bins = np.linspace(min(photons_eta), max(photons_eta), 21))
p1, bins4 = P1
f4, axs4 = plt.subplots(figsize=(14, 7))
axs4.set_yscale('log')
hep.histplot(p1, bins4, yerr=True, ax=axs4, histtype = 'fill')
plt.xlabel('Photons eta')
plt.ylabel('Number of photons per bin')
plt.title('Photons pseudorapidity distribution')
plt.savefig('/grid_mnt/data__data.polcms/cms/spallacci/CMSSW_11_3_4/src/EFT2Obs/graphs/photons_eta_cw.png')