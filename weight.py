import numpy as np 
from lhereader import LHEReader
import matplotlib.pyplot as plt
import mplhep as hep

reader = LHEReader('/grid_mnt/data__data.polcms/cms/spallacci/CMSSW_11_3_4/src/EFT2Obs/test-WG-LO/events_2.lhe')

res = []
photpt = []
inv_cw = np.linalg.inv(np.array([[0.005, 0.000025], 
                   [0.01, 0.0001]]))

cw = [0, 0.01, 0.03, 0.05]

for iev, event in enumerate(reader):

    phot = filter(lambda x: abs(x.pdgid) == 22, event.particles)
    mu = np.array([[event.weights[1]/event.weights[0]-1],
                   [event.weights[2]/event.weights[0]-1]])
    res.append(np.dot(inv_cw, mu))

    for x in phot:
        photpt.append(x.p4().pt)

f_photpt = np.array(photpt)

h = []
bins = np.linspace(min(photpt), max(photpt), 21)
small_bin_edges = np.linspace(min(photpt), bins[8], 13) 
medium_bin_edges = np.linspace(bins[8], bins[12], 7)  # Medium-sized bins
large_bin_edges = np.linspace(bins[12], bins[17], 3) 
last = np.linspace(bins[17], bins[-1], 2) 

# Combine all edges into one array, avoiding duplicate edges
bin_edges = np.concatenate((small_bin_edges, medium_bin_edges[1:], large_bin_edges[1:], last[1:]))


for n in cw:

    w = [float(1 + res[i][0]*n + res[i][1]*n**2) for i in range(len(res))]
    d = {f_photpt[i] : w[i] for i in range(len(res))}


    # Categorize data into bins
    binned_data = [f_photpt[(f_photpt >= bin_edges[i]) & (f_photpt < bin_edges[i+1])] for i in range(len(bin_edges)-1)]

    # For the last bin, you might want to include the right edge
    binned_data[-1] = np.append(binned_data[-1], f_photpt[f_photpt == bin_edges[-1]])

    hf = []
    for i in binned_data:
        if len(i) == 0:
            hf.append(0)
        else: 
            counter = 0
            for g in i:    
                counter += d[g]
            hf.append(counter)
    h.append(hf)


    
plt.style.use(hep.style.CMS)

f2, axs = plt.subplots(figsize=(14, 7))
hep.histplot(h, bins = bin_edges, ax=axs, yerr = True, label = [f'CW={cw[0]}', f'CW={cw[1]}', f'CW={cw[2]}', f'CW={cw[3]}'])
plt.xlabel('Photons pt')
axs.legend()
axs.set_yscale('log')
plt.ylabel('Weighted Number of photons per bin')
plt.title('Weighted Number of photons per bin for different cw')
plt.savefig('/grid_mnt/data__data.polcms/cms/spallacci/CMSSW_11_3_4/src/EFT2Obs/graphs/photons_pt_diffcw_dfbinsize2.png')

h1 = np.zeros((len(h), len(h[0])))
for i in range(len(h)):
    for j in range(len(h[i])):
        if h[0][j] == 0:
            h1[i][j] = 0
        else:
            h1[i][j] = float(h[i][j])/float(h[0][j])



fig, (ax, rax) = plt.subplots(nrows = 2, ncols= 1, gridspec_kw={"height_ratios": (3, 1), "hspace": 0.05}, sharex=True)
hep.histplot(
    h,
    bins=bin_edges,
    ax=ax,
    yerr = True,
    label=[f'CW={cw[0]}', f'CW={cw[1]}', f'CW={cw[2]}', f'CW={cw[3]}'],
)

for ratio in h1:
    hep.histplot(
        ratio,
        bins=bin_edges,
        ax=rax,
        histtype="step"
    )
ax.set_yscale('log')
ax.legend()
ax.set_ylabel('a.u.')
rax.set_ylabel('Ratio to SM')
rax.set_xlabel('Transverse Momentum')
plt.savefig('/grid_mnt/data__data.polcms/cms/spallacci/CMSSW_11_3_4/src/EFT2Obs/graphs/photons_pt_diffcw_stacked_dfbinsize2.png')



    