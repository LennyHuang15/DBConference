#-*- coding:utf-8 -*-
import http.server as BaseHTTPServer
import sys
import os
import cgi
import json
import urllib

class RequestHandler(BaseHTTPServer.BaseHTTPRequestHandler):
	'''处理请求并返回页面'''
	
	title = 'hello'
	# 页面模板
	page = ''
	
	# 处理一个GET请求
	def do_GET(self):
		try:
			full_path = os.getcwd() +"/pages"+ self.path
			print(full_path)
			if(not os.path.exists(full_path)):
				raise ServerException("'{0}' not found".format(self.path))
			elif(os.path.isfile(full_path)):
				self.handle_file(full_path)
			# not a file
			elif(os.path.isdir(full_path)
					and os.path.isfile(full_path + "/index.html")):
				self.handle_file(full_path+"/index.html")
			else:
				raise ServerException("Unknown object'{0}'".format(self.path))
		except Exception as e:
			self.handle_error("do_GET\n" + str(e));
		
	def do_POST(self):
		try:
			print("do_POST")
			request_str = self.rfile.read(int(self.headers['Content-Length']))
			request = json.loads(request_str.decode('utf-8'))
			#print(request)
			content = json.dumps(getdata(request)).encode('utf-8')
			#print(content)
			self.send_response(200)
			self.send_header("Content-Type", "application/json")
			self.send_header("Content-Length", str(len(content)))
			self.end_headers()
			self.wfile.write(content)
		except Exception as e:
			print(e)
			self.handle_error("do_POST\n" + str(e));
	
	'''def create_page(self):
		values = {
			'title'	:	self.title
		}
		return self.page.format(**values).encode('utf-8')'''
	
	def send_content(self, content, status=200):
		self.send_response(status)
		self.send_header("Content-Type", "text/html")
		self.send_header("Content-Length", str(len(content)))
		self.end_headers()
		self.wfile.write(content)
	
	def handle_file(self, full_path):
		try:
			with open(full_path, 'rb') as reader:
				content = reader.read()
			# assert content is bytes
			self.send_content(content)
		except IOError as e:
			self.handle_error("'{0}' cannot be read: {1}".format(self.path, e))
	
	error_page = '''\
<html>
<body>
<h1>Error Accessing {path}</h1>
<p>{e}</p>
</body>
</html>
'''
	def handle_error(self, e):
		content = self.error_page.format(
								path=self.path,
								e = e).encode('utf-8')
		self.send_content(content, 404)

#----------------------------------------------------------------------
class ServerException(Exception):
	'''exception inside server'''
	pass

dict_pc = {}

def getdata(request):
	print(request)
	if(request['title'] == "citations"):
		return getCitations(request['conference'], int(request['year']), int(request['number']))
	elif(request['title'] == "pc_topic"):
		return getPcTopic(request['conference'], request['year'])
	'''elif(request['title'] == ""):
	elif(request['title'] == ""):'''
	
def getPcTopic(conf, year):
	global dict_pc
	path = "../dataset/"
	os.system('python getTopic.py '+conf+' '+year)
	lines = []
	with open(path+"Role.csv", 'r', encoding='utf-8') as f:
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
	response = {'pc':[], 'topic':[]}
	max_topic_id = 0
	for pid in pids:
		if(pid in dict_pc):
			info = dict_pc[pid]
		else:
			info = ('Unknown', 'Unknown')
		response['pc'].append({'pid': pid, 'name': info[0], 'affiliation': info[1], 'citations_topic':[]})
		for i in range(40):
			response['pc'][-1]['citations_topic'].append(0)
		with open("../citations/paper_topic/"+pid+".csv", 'r', encoding='utf-8') as f:
			lines = f.readlines()
		for line in lines:
			st = line.strip().split(',')
			ct = st[5]
			if(ct != '*' and len(st) >= 7):
				ct = int(ct)
				id_topic = int(st[6])
				if(id_topic > max_topic_id):
					max_topic_id = id_topic
				response['pc'][-1]['citations_topic'][id_topic] += ct
	response['topic'] = list(range(max_topic_id+1))
	'''print("max_topic_id")
	print(max_topic_id)
	for i in range(len(pids)):
		response['pc'][i]['citations_topic'] = response['pc'][i]['citations_topic'][:max_topic_id+1]
	print("pc:")
	for pc in response['pc']:
		print(pc)
	print("topic:")
	for topic in response['topic']:
		print(topic)'''
	return response
	
def getCitations(conf, year, num):
	global dict_pc
	path = "../dataset/"
	#os.system('python '+ path+'PCcitation.py')
	file = open(path + "Role.csv", 'r', encoding='utf-8')
	pclines = file.readlines()
	file.close()
	file = open(path + 'PCCitations.csv', 'r', encoding = 'utf-8')
	lines = file.readlines()
	file.close()
	
	pcCitations = {}
	citations = []
	for line in lines[1:]:
		st = line.strip().split(',')
		pcCitations[st[0]] = int(st[2])
	for line in pclines[1:]:
		st = line.strip().split(',')
		mconf = st[2]
		myear = int(st[3])
		if(mconf == conf and myear == year):
			pid = st[0]
			if(not pid in pcCitations.keys()):
				print(pid + " not found")
			else:
				if(pid in dict_pc):
					info = dict_pc[pid]
				else:
					info = ('Unknown', 'Unknown')
				citations.append({'pid':pid, 'citations':pcCitations[pid],\
								'name': info[0], 'affiliation': info[1]})
	citations = sorted(citations, key=lambda pc: pc['citations'], reverse=True)
	#print(len(citations))
	#for item in citations:
		#print(item['pid'] + ' -> ' + str(item['citations']))
	return citations[:num]
		
def initResearcherInfo():
	global dict_pc
	file = open('../dataset/Researcher.csv', 'r', encoding = 'utf-8')
	lines = file.readlines()
	file.close()
	for line in lines[1:]:
		pid, name, affiliation = line.strip().split(',')
		dict_pc[pid] = (name, affiliation)
		
def keyRole(role):
	return role == 'Group Leaders' or role == "Associate Editors" or role == 'Area Chairs' or role == 'Vicechairs'
		
def init():
	initResearcherInfo()

if __name__ == '__main__':
	init()
	#getCitations('sigmod', 2018, 20)
	getPcTopic('sigmod', '2018')
	serverAddress = ('', 8080)
	server = BaseHTTPServer.HTTPServer(serverAddress, RequestHandler)
	server.serve_forever()