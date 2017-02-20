import numpy as np
import cv2
import os

os.environ['GLOG_minloglevel'] = '3' 


import caffe
import sys
import glob

from google.protobuf import text_format
from caffe.proto import caffe_pb2


def get_labelname(labelmap, labels):
    num_labels = len(labelmap.item)
    labelnames = []
    if type(labels) is not list:
        labels = [labels]
    for label in labels:
        found = False
        for i in xrange(0, num_labels):
            if label == labelmap.item[i].label:
                found = True
                labelnames.append(labelmap.item[i].display_name)
                break
        assert found == True
    return labelnames


def init_():
	caffe.set_device(0)
	caffe.set_mode_gpu()

	#label info
	labelmap_file = 'labelmap_voc.prototxt'
	file = open(labelmap_file, 'r')
	labelmap = caffe_pb2.LabelMap()
	text_format.Merge(str(file.read()), labelmap)
	model_def = './deploy.prototxt'
	model_weights = 'person_new.caffemodel'
	net = caffe.Net(model_def,      # defines the structure of the model
			model_weights,  # contains the trained weights
			caffe.TEST)     # use test mode (e.g., don't perform dropout)

	# input preprocessing: 'data' is the name of the input blob == net.inputs[0]
	transformer = caffe.io.Transformer({'data': net.blobs['data'].data.shape})
	transformer.set_transpose('data', (2, 0, 1))
	transformer.set_mean('data', np.array([104,117,123])) # mean pixel
	transformer.set_raw_scale('data', 255)  # the reference model operates on images in [0,255] range instead of [0,1]
	transformer.set_channel_swap('data', (2,1,0))  # the reference model has channels in BGR order instead of RGB

	# set net to batch size of 1
	image_resize = 300
	net.blobs['data'].reshape(1,3,image_resize,image_resize)
	return labelmap, net, transformer


def detect(fname, labelmap, net, transformer):
	image = caffe.io.load_image(fname)
	rows, cols = image.shape[:2]

	transformed_image = transformer.preprocess('data', image)
	net.blobs['data'].data[...] = transformed_image

	# Forward pass.
	detections = net.forward()['detection_out']

	# Parse the outputs.
	det_label = detections[0,0,:,1]
	det_conf = detections[0,0,:,2]
	det_xmin = detections[0,0,:,3]
	det_ymin = detections[0,0,:,4]
	det_xmax = detections[0,0,:,5]
	det_ymax = detections[0,0,:,6]

	# Get detections with confidence higher than 0.6.
	top_indices = [i for i, conf in enumerate(det_conf) if conf >= 0.5]

	top_conf = det_conf[top_indices]
	top_label_indices = det_label[top_indices].tolist()
	top_labels = get_labelname(labelmap, top_label_indices)
	top_xmin = det_xmin[top_indices]
	top_ymin = det_ymin[top_indices]
	top_xmax = det_xmax[top_indices]
	top_ymax = det_ymax[top_indices]

	
	dets = []
	for i in xrange(top_conf.shape[0]):
	    xmin = int(round(top_xmin[i] * image.shape[1]))
	    ymin = int(round(top_ymin[i] * image.shape[0]))
	    xmax = int(round(top_xmax[i] * image.shape[1]))
	    ymax = int(round(top_ymax[i] * image.shape[0]))
	    score = top_conf[i]
	    label = int(top_label_indices[i])
	    label_name = top_labels[i]
	    if (label_name.find('person') <0):
	    	continue
	    dets.append([xmin, xmax, ymin, ymax])

	return dets

init_()
labelmap, net,transformer = init_()

image_dir = './data/images/'
fnames = glob.glob(image_dir + '*jpg')
for fname in fnames:
	dets = detect(fname, labelmap, net, transformer)

	im = cv2.imread(fname)
	for det in dets:
		cv2.rectangle(im, (det[0],det[2]), (det[1], det[3]), (0,255,0),3)

	cv2.imwrite(fname, im)
	#cv2.imshow("c", im)
	#cv2.waitKey(0)
