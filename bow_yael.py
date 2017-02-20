import cv2
import numpy as np
import glob
import pickle
import random

import scipy.io as spio
import os
import numpy as np
from yael import ynumpy
from matplotlib import pyplot as plt

def make_square(im):
    wider = False
    r1,c1 = 400., 400.
    r,c = im.shape[0], im.shape[1]
    r = float(r)
    im_out = np.ones((r1,c1,3), dtype=np.uint8)
    im_out[:, :, 0] = np.amax(im[:, :, 0])
    im_out[:, :, 1] = np.amax(im[:, :, 1])
    im_out[:, :, 2] = np.amax(im[:, :, 2])

    if (r/c > r1/c1):
        scale = r1/r
        wider = True
    else:
        scale = c1/c
    if (scale>1):
        scale = 1.
    else:
        im = cv2.resize(im,(0,0), fx = scale,fy = scale)
    r,c = im.shape[0],im.shape[1]

    c1 = int(c1)
    c = int(c)
    startc = int((c1-c)/2)
    stopc = int((c1+c)/2)

    r1 = int(r1)
    r = int(r)
    startr = int((r1-r)/2)
    stopr = int((r1+r)/2)

    im_out[startr:stopr,startc:stopc,:] = im

    return im_out;


def get_distances(train_images):
	surf = cv2.SURF(hessianThreshold=500, extended=True)
	image_descs = []
	for fnames in train_images:
		try:
    			img = cv2.imread(fnames,0);
		    	kp, des = surf.detectAndCompute(img, None)			
		except:
			continue
		image_descs.append(des)


	all_desc= np.vstack(image_descs)

	k = 128
	n_sample = k * 500

	sample = all_desc
	sample = sample.astype('float32')

	mean = sample.mean(axis = 0)
	sample = sample - mean
	cov = np.dot(sample.T, sample)

	eigvals, eigvecs = np.linalg.eig(cov)
	perm = eigvals.argsort()
	pca_transform = eigvecs[:, perm[32:128]]

	sample = np.dot(sample, pca_transform)
	gmm = ynumpy.gmm_learn(sample, k)

	image_fvs = []
	for image_desc in image_descs:
		image_desc = np.dot(image_desc - mean, pca_transform)
		fv = ynumpy.fisher(gmm, image_desc, include = 'mu')
		image_fvs.append(fv)

	image_fvs = np.vstack(image_fvs)
	image_fvs = np.sign(image_fvs) * np.abs(image_fvs) ** 0.5
	norms = np.sqrt(np.sum(image_fvs ** 2, 1))
	image_fvs /= norms.reshape(-1, 1)

	image_fvs[np.isnan(image_fvs)] = 100

	query_imnos = range(0,len(image_fvs)-1);
	query_fvs = image_fvs#[query_imnos]

	results, distances = ynumpy.knn(query_fvs, image_fvs, nnn = len(image_fvs))
	s_results = np.argsort(results, axis = 1)
	s_distances = distances*0
	for i in range(distances.shape[0]):
	    s_distances[i,:] = distances[i,s_results[i,:]]
	
	return s_distances


fpath = '/tmp/crap/'
dst = fpath + '/output/';
os.system('mkdir -p ' + dst)
fnames_vec = glob.glob(fpath + "/*jpg");
fnames_vec = sorted(fnames_vec)
print len(fnames_vec)
distances = get_distances(fnames_vec)
print (distances[0,:20]*100).astype(np.int32)
