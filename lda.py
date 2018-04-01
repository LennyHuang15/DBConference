#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import io
#sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf8')
import random

def paperBatch(conf, year, size):
	file = open(conf+'_pid.txt','r',encoding='utf-8')
	inlines = file.readlines()
	file.close()
	#researchers
	pids = []
	getYear = 0
	for line in inlines:
		#print(line)
		if(len(line) <= 0):continue
		if(not getYear):
			if(line[0] == '#' and line[1:-1] == year):
				getYear = 1
			continue
		if(line[0] == '#' and line[1:-1] != year):break
		if(line[0] == '-'):continue
		pid = line.strip().split('*')
		if(len(pid[0]) > 0):
			pids.append(pid[0])
			#print(pid[0])
	#papers
	papers = []
	num = int(2*size / len(pids))
	if(num < 5):num = 5
	for i in range(size):
		if(i % 100 == 0):print(i)
		pid = random.choice(pids)
		try:
			file = open('names/'+pid+'.csv','r',encoding='utf-8')
			line = file.readline()
			for j in range(random.randint(0, num-1)):
				line = file.readline()
			st = line.split(',')
			file.close()
			if(len(st) <= 3 or st[0] == '*' or st[2] == '*'):
				i -= 1
				continue
			papers.append(st[0] + ',' + st[2])
		except Exception as e:
			i -= 1
			print(e)
			continue
	print('total papers: ' + str(len(papers)))
	return papers
	

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation as LDA

if __name__ == '__main__':
	corpus = paperBatch('sigmod','2018', 1000)
	cntVec = CountVectorizer()
	cntTf = cntVec.fit_transform(corpus)
	#lda = LDA(n_topics=24, learning_offset=50.,random_state=0)
	#docres = lda.fit_transform(cntTf)
	
