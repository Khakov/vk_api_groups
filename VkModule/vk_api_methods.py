import re
import vk
def init_session():
    session = vk.Session()
    return vk.API(session)

def get_user_id_by_unformat_string(unformat_string):
    match = re.search(r'(?:http(?:s?)://)?(?:.*/)?(?P<remove_person_id>.*)', unformat_string)
    remove_person_id = match.group('remove_person_id')
    if remove_person_id.startswith('id') and remove_person_id[2].isdigit():
        remove_person_id = remove_person_id.replace('id', '')
    else:
        api = init_session()
        remove_person_id = api.users.get(user_ids=remove_person_id)[0]['uid']
    return remove_person_id


class Changs:
    delete_group = set()
    delete_group_red = set()
    new_persons = set()
    new_persons_red = set()
    date = ''


def get_group_name(id):
    api = init_session()
    name = api.groups.getById(group_id=id)
    name = name[0]
    name = name[u'name']
    return name


def set_new_users(group_id):
    api = init_session()
    members = api.groups.getMembers(group_id=group_id)
    count = int(members[u'count'])
    users = set(members[u'users'])
    number = 1000
    while count - number > 0:
        members = api.groups.getMembers(group_id=group_id, offset=number)
        users.update(set(members[u'users']))
        number += 1000
    return users


def get_diff(users, diff_set):
    return users.difference(diff_set)