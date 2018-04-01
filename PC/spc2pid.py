import os
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf8')

def procConf(conf):
	read = open(conf+'_pid.txt','r',encoding='utf-8')
	lines = read.readlines()
	read.close()
	dict = {}
	year = 2018
	for line in lines:
		if(line[0]=='#'):
			year = int(line[1:-1])
			dict[year] = {}
		elif(len(line) > 1 and line[0] != '-'):
			st = line.strip().split('*')
			if(len(st[0]) <= 0):
				dict[year][st[1]] = ''
			else:
				dict[year][st[1]] = st[0]
	print(conf)
	print(dict[2018])
	return dict

def toPid():
	read = open('spc.csv','r')#,encoding='utf-8')
	inlines = read.readlines()
	read.close()
	outlines = ''
	conf = 'sigmod'
	dict = procConf(conf)
	switch = False
	for line in inlines:
		if(line[0]==','):
			outlines += line
			switch = True
			continue
		sts = line.strip().split(',')
		if(switch):
			print(sts[0] + ' vs ' + conf)
			if(sts[0] != conf):
				conf = sts[0]
				dict = procConf(conf)
			switch = False
		if(len(sts[-1]) <= 0):
			outlines += sts[0] +','+sts[1] +','+sts[2] +',*\n'
			continue
		name = sts[-1]
		if not name in dict[int(sts[1])]:
			pid = ''
		else:
			pid = dict[int(sts[1])][name]
		if(len(pid)<=0):
			pid = '*'+name
		outlines += sts[0] +','+sts[1] +','+sts[2] +','+ pid+'\n'
	outfile = open('spc_pid.csv','w')
	outfile.write(outlines)
	outfile.close()
	
if __name__ == '__main__':
	toPid()
	