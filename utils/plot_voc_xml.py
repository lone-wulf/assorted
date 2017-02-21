import cv2
import numpy as np

import os
from glob import glob
from random import shuffle
from bs4 import BeautifulSoup


def load_annotation(annotation_filename):
    """
    Load annotation file for a given image.
    Args:
        img_name (string): string of the image name, relative to
            the image directory.
    Returns:
        BeautifulSoup structure: the annotation labels loaded as a
            BeautifulSoup data structure
    """
    xml = ""
    with open(annotation_filename) as f:
        xml = f.readlines()
    xml = ''.join([line.strip('\t') for line in xml])
    return BeautifulSoup(xml)

def parse_annotations(ann_files, src_dir, N=13, dst_dir = '/tmp/images/'):
	colors = [(0,0,255), (0, 255, 0)]
        for item in ann_files:
	    flag = 0
            anno = load_annotation(item)
            objs = anno.findAll('object')
            for obj in objs:
                obj_names = obj.findChildren('name')
                for name_tag in obj_names:
		    #ii = str(name_tag.contents[0]) == 'horse'
		    ii = 1
                    if 1:
                        fname = anno.findChild('filename').contents[0]
			
                        bbox = obj.findChildren('bndbox')[0]
                        xmin = int(bbox.findChildren('xmin')[0].contents[0])
                        ymin = int(bbox.findChildren('ymin')[0].contents[0])
                        xmax = int(bbox.findChildren('xmax')[0].contents[0])
                        ymax = int(bbox.findChildren('ymax')[0].contents[0])
			if not flag:
				im = cv2.imread(src_dir + fname)
				ofile = dst_dir + fname
				flag = 1
			
			color = colors[ii]
			if ii:
				cv2.rectangle(im, (xmin, ymin), (xmax, ymax), color, 1)
			else:
				cv2.circle(im, ((xmin+xmax)/2, (ymin+ymax)/2), 5, (255,0,0),-1)
				cv2.rectangle(im, (xmin, ymin), (xmax, ymax), color, 1)
  	    cv2.imwrite(ofile, im)
	    print ofile
src_dir = './data/JPEGImages/'
ann_files = glob('./data/Annotations/*xml');
shuffle(ann_files)
parse_annotations(ann_files, src_dir, N=13)
