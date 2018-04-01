import sys
import io
import os
sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf8')

path = '../citations'
def countPC(name): #return n_paper, sum_citations
	file = open(path+'/'+name,'r',encoding = 'utf-8')
	lines = file.readlines()
	file.close()
	citations = 0
	for line in lines:
		ct = line.split(',')[-1][:-1]
		if(ct != '*'):
			citations += int(ct)
	return len(lines), citations

def countPath():
	files= os.listdir(path) #得到文件夹下的所有文件名称
	lines = ''
	for file in files: #遍历文件夹  
		if not os.path.isdir(file): #判断是否是文件夹，不是文件夹才打开  
			pid = file.split('.')[0]
			cnt, citations = countPC(file)
			print(pid+': '+str(cnt)+','+str(citations))
			lines += pid + ',' +str(cnt)+ ',' +str(citations)+'\n'
	outfile = open('PCCitations.csv','w')
	outfile.write(lines)
	outfile.close()
	
if __name__ == '__main__':
	countPath()