#-*- coding:utf-8 -*-
import sys
import os
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf8')
import random

def paperBatch(conf, year, size):
	#pids
	num_each_pc = 3
	num_pc = int(size / num_each_pc) + 50
	pids = []
	inlines = []
	with open("dataset/Researcher.csv", 'r', encoding='utf-8') as f:
		inlines = f.readlines()
	inlines = random.sample(inlines[1:], num_pc)
	for line in inlines:
		pids.append(line.split(',')[0])
	print(pids)
	#papers
	papers = []
	idx_pid = -1
	cnt_paper = 0
	cnt_pid_paper = 0
	lines = []
	while(True):
		if(cnt_pid_paper >= num_each_pc or cnt_pid_paper >= len(lines)):
			# change another pc
			idx_pid += 1
			pid = pids[idx_pid]
			cnt_pid_paper = 0
			try:
				file = open('citations/'+pid+'.csv','r',encoding='utf-8')
				lines = file.readlines()
				file.close()
				if(len(lines) > num_each_pc + 5):
					lines = random.sample(lines, num_each_pc + 5)
				continue
			except Exception as e:
				print(e)
				lines = []
				continue
		st = lines[cnt_pid_paper].split(',')
		cnt_pid_paper += 1
		if(len(st) <= 3 or st[0] == '*' or st[2] == '*'):
			continue
		papers.append(st[0] + ',' + st[2])
		cnt_paper += 1
		if(cnt_paper % 100 == 0):print(cnt_paper)
		if(cnt_paper >= size): return papers

def glPapers(conf, year):
	lines = []
	papers = []
	with open("dataset/Role.csv", 'r', encoding='utf-8') as f:
		lines = f.readlines()
	reach = False
	pids = []
	for line in lines[1:]:
		pid, role, _conf, _year = line.strip().split(',')
		if(_conf == conf and _year == year and keyRole(role)):
			reach = True
			pids.append(pid)
		else:
			if(reach):
				break
	print("%s[%s]:\n"%(conf, year) + str(pids))
	papers = []
	for pid in pids:
		papers += getPaperCont(pid)
	return papers
	

def keyRole(role):
	#return role == 'Vicechairs'#'Group Leaders'
	return 'Chairs' in role
	
def getPaperCont(pid):
	file = open('citations/'+pid+'.csv','r',encoding='utf-8')
	lines = file.readlines()
	file.close()
	papers = []
	for idx in range(len(lines)):
		line = lines[idx]
		st = line.split(',')
		if(len(st) <= 3 or st[0] == '*' or st[2] == '*'):
			continue
		papers.append((pid, idx, st[0] + ',' + st[2]))
	print("%s papers: %d"%(pid, len(papers)))
	return papers

if __name__ == '__main__':
	#papers = paperBatch('sigmod','2018',1000)
	papers = glPapers('icde','2017')
	print("total papers: %d"%(len(papers)))
	random.shuffle(papers)
	
	outfile = open("python-LDA/data/train.dat", 'w', encoding='utf-8')
	idxfile = open("python-LDA/data/paper_index.dat", 'w', encoding='utf-8')
	for pid, idx, paper in papers:
		paper_train = paper.replace(',',' ').replace(';',' ').replace(':',' ').replace('.',' ').replace('…',' ')\
					.replace('\"',' ').replace('“',' ').replace('”',' ').replace('(',' ').replace(')',' ')
		outfile.write(paper_train+'\n')
		idxfile.write(pid+','+str(idx)+'\n')
	outfile.close()
	idxfile.close()
	