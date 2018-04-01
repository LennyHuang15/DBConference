API:

1. get the conf's top-m pc's citations
title: 'citation'
conference: conf,
year: year,
number: m

responseData:
[{'pid':, 'citations':,'name':, 'affiliation':}, ...]

2. get group leaders/associate editors ' citations on topics
title: 'pc_topic'
conference: conf,
year: year,

responseData:
{'pc': [{'pid':, 'name':, 'affiliation':, 'citations_topic':[(citations of each topic of the same index)]}, ...]
'topic':[(topic_name)]}
