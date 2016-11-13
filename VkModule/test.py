import vk
import json

session = vk.Session()
api = vk.API(session)
names = api.groups.getById(group_id='itis_kpfu')
names = names[0]
names = names[u'name']
print names
# users = json.dump(names,fp='' ensure_ascii=False, )
# users = unicode(encoding='UTF-8',  names)
