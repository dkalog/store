import matplotlib.pyplot as plt
import numpy as np
from os import path
import os

def histogram(abspt,frequency,bins,angerror,title=None,typE="angular"):
	
	if path.exists(os.path.join(abspt,'plots')) == False:
		os.mkdir(os.path.join(abspt,'plots'))

	fig=plt.figure(figsize=(14,5))
	freq, binS, patches = plt.hist(angerror, bins=bins)
	plt.gca().set(title=title, ylabel='Frequency',xlabel=typE+' error')
	#plt.xticks(range(int(max(angerror))))
	bin_size = (max(angerror) - min(angerror))/bins
	print(f"Bin size = {bin_size}")

	bin_centers = np.diff(binS)*0.5 + binS[:-1]
	n = 0
	for fr, x, patch in zip(freq, bin_centers, patches):
	  height = int(freq[n])
	  plt.annotate("{}".format(height),
	               xy = (x, height),             # top left corner of the histogram bar
	               xytext = (0,0.2),             # offsetting label position above its bar
	               textcoords = "offset points", # Offset (in points) from the *xy* value
	               ha = 'center', va = 'bottom'
	               )
	  n = n+1
	plt.ylim(0,len(angerror))
	plt.savefig(os.path.join(os.path.join(abspt,'plots'),title+'_'+typE+'.png'))
	plt.show()


def scatterplot(abspt,angerror,imageID,color='b',title=None,typE="angular"):

	if path.exists(os.path.join(abspt,'plots')) == False:
		os.mkdir(os.path.join(abspt,'plots'))
	fig=plt.figure()

	ax=fig.add_subplot(111)
	plt.gca().set(title=title, ylabel='Image id',xlabel=typE+' error')
	plt.scatter(angerror,imageID,5,color=color)

	plt.savefig(os.path.join(os.path.join(abspt,'plots'),title+'_'+typE+'.png'))
	plt.show()

	