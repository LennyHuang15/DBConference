file = open('ConfTopic1.csv','r',encoding='utf-8')
inline = file.readlines()
file.close()
outline = ''
for line in inline:
	outline += 'icde,2017,'
	outline += line[:-1].replace(',',';') + ',\n'
file = open('ConfTopic1.csv','w')
file.write(outline)
file.close()