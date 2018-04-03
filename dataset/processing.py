'''file = open('Researcher_Loc_Linkedin.csv','r',encoding='utf-8')
inline = file.readlines()
file.close()
file = open('Researcher_Loc_Linkedin_1.csv','a',encoding='utf-8')
for line in inline:
	sts = line.strip().split(',')
	m_sts = []
	for st in sts:
		st = st.split(';')
		m_st = []
		for s in st:
			m_st.append(s.strip())
		m_sts.append(';'.join(m_st))
	file.write(','.join(m_sts) + '\n')
file.close()'''
file = open('Researcher_Loc_Linkedin_1.csv','r',encoding='utf-8')
inline = file.readlines()
file.close()
locs = set()
for line in inline:
	st = line.strip().split(',')[-1].split(';')[-1]
	if not st in locs:
		locs.add(st)
file = open('Locs.csv','w',encoding='utf-8')
for loc in sorted(locs):
	file.write(loc+'\n')
file.close()

