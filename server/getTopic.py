import sys
def getTopic(conf, year):
	path = "../python-LDA/LDA-"+conf+year+"/"
	file = open(path + "paper_index.dat", 'r', encoding='utf-8')
	lines = file.readlines()
	file.close()
	paper_index = []
	for line in lines:
		st = line.strip().split(',')
		paper_index.append((st[0], int(st[1])))
	
	file = open(path + "tmp/model_tassign.dat", 'r', encoding='utf-8')
	sts = file.read().split()
	file.close()
	papers = []
	for st in sts:
		tmp = st.split(':')
		papers.append(tmp[1])
	
	pc_paper = {}
	for i in range(len(paper_index)):
		pid, idx = paper_index[i]
		if(not pid in pc_paper):
			pc_paper[pid] = papers_pc(pid)
		pc_paper[pid][idx] = pc_paper[pid][idx][:-1] + ','+papers[i]+'\n'
	
	for pid, lines in pc_paper.items():
		file = open("../citations/paper_topic/"+pid+".csv", 'w', encoding='utf-8')
		for line in lines:
			file.write(line)
		file.close()
	
		
def papers_pc(pid):
	file = open("../citations/"+pid+".csv", 'r', encoding='utf-8')
	lines = file.readlines()
	file.close()
	return lines

if __name__ == "__main__":
	getTopic(sys.argv[1], sys.argv[2])
