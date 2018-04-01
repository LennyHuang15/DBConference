
def invertedTopic():
	file = open("ConfTopic_pid.csv", 'r', encoding="utf-8")
	lines = file.readlines()
	file.close()
	dict_topics = {}
	for line in lines[1:]:
		conf, year, topic, pid = line.split(',')
		if(not topic in dict_topics):
			dict_topics[topic] = []
		dict_topics[topic].append((conf, year))
	file = open("TopicInverted.csv", 'w', encoding='utf-8')
	ordered_dict = sorted(dict_topics.items())
	for key, value in ordered_dict:
		file.write(key + '\n')
		for conf, year in value:
			file.write(conf+year+" ")
		file.write("\n\n")
	file.close()

if __name__ == "__main__":
	invertedTopic()