from __future__ import print_function

# import gensim
# from gensim import *
# from gensim.models.word2vec import Word2Vec
import sys
# from gensim.models.keyedvectors import KeyedVectors, Vocab
from numpy import array
from scipy.cluster.vq import vq, kmeans, whiten
import numpy as np
# from wordvec_model import *
import fileinput
from sklearn.decomposition import PCA


vec =sys.argv[1]
out = sys.argv[2]
newDim = sys.argv[3]

X = []
vocabulary = []
header = None
for line in fileinput.input(vec):
	line = ' '.join(line.split())

	if header == None:
		header = '{} {}'.format(line.split()[0],newDim)

	else:
		vocabulary.append(line.split(' ')[0])
		X.append(list(float(x) for x in list(line.split()[1:])))

fileinput.close()

X = np.array(X)
pca = PCA(n_components=100)
X = pca.fit_transform(X)

out = open(out,'w')

out.write('{}\n'.format(header))
for i in range(len(vocabulary)):
	out.write('{} {}\n'.format(vocabulary[i], ' '.join(list(str(round(x,5)) for x in X[i]))))

out.close()


