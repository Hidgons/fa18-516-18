from mongoengine import *
import datetime
from pymongo import MongoClient

from cloudmesh_data.data.Config import Config
from cloudmesh_data.data.util.retrieve_yaml_definition_properties import generate
from cloudmesh_data.data.util import get_file_size_and_checksum

#
# BUG: needs to come from config
#
config = Config()
connect(config.database()['database'], host=config.database()['host'], port=config.database()['port'])

client = MongoClient('localhost', 27017)
db = client['mongoengine_test']

filecollection = db.get_collection("file")
usercollection = db.get_collection("user")
vdircollection = db.get_collection("virtualdirectory")

# To print all records for file table
# for file in vdircollection.find():
# print(file)
# To delete all records
# myquery = {}
# usercollection.delete_many({})


fileproperty = generate("File")
i = 0
while i < len(fileproperty):
    # print(fileproperty[i])
    i += 1

userproperty = generate("User")
j = 0
while j < len(userproperty):
    # print(userproperty[j])
    j += 1

vdirproperty = generate("Virtualdirectory")
i = 0
while i < len(vdirproperty):
    # print(vdirproperty[i])
    i += 1


class File(Document):
    name = StringField(primary_key=True)
    endpoint = StringField()
    checksum = StringField()
    size = StringField()
    timestamp = DateTimeField(default=datetime.datetime.now)
    last_modified = DateTimeField(default=datetime.datetime.now)
    user_uuid = StringField()
    file_content = FileField()


class User(Document):
    uuid = StringField(primary_key=True)
    username = StringField()
    group = StringField()
    role = StringField()
    resource = StringField()
    context = StringField()
    description = StringField()
    firstname = StringField()
    lastname = StringField()
    publickey = StringField()
    email = StringField()


class Virtualdirectory(Document):
    name = StringField(primary_key=True)
    description = StringField()
    host = StringField()
    location = StringField()
    protocol = StringField()
    credential = StringField()


def save_file_to_db(provider, file_path, filename, user_uuid):
    checksum_value = get_file_size_and_checksum.md5(file_path)
    file_size = get_file_size_and_checksum.file_size(file_path)
    content = open(file_path, 'rb')

    file = File(
        name=filename,
        endpoint=provider,
        checksum=checksum_value,
        size=file_size,
        timestamp=datetime.datetime.now,
        last_modified=datetime.datetime.now,
        user_uuid=user_uuid
    )
    if filename.endswith('.png'):
        file.file_content.put(content, content_type='image/jpeg')
    elif filename.endswith('.txt') or filename.endswith('.docx'):
        file.file_content.put(content, content_type='text')

    file.save()


def update_user_for_file(user_uuid, filename):
    myquery = {"name": filename}
    newvalues = {"$set": {"user_uuid": user_uuid}}
    filecollection.update_one(myquery, newvalues)

    # print "customers" after the update:
    # for x in filecollection.find():
    #   print(x)


def save_user_to_db(profile):
    user = User(
        uuid=profile.get_uuid(),
        username=profile.get_username(),
        group=profile.get_group(),
        role=profile.get_role(),
        resource=profile.get_resource(),
        context=profile.get_context(),
        description=profile.get_description(),
        firstname=profile.get_firstname(),
        lastname=profile.get_lastname(),
        publickey=profile.get_publickey(),
        email=profile.get_email()
    )

    user.save()


def get_profiles():
    return list(usercollection.find({}, {'_id': False}))


def get_profile_by_uuid(uuid):
    myquery = {"_id": uuid}

    user = usercollection.find(myquery)
    profile = []
    for x in user:
        profile.append(x)

    return profile


def save_vdir_to_db(name, description, host, location):
    vdir = Virtualdirectory(
        name=name,
        description=description,
        host=host,
        location=location,
        protocol='',
        credential=''
    )
    vdir.save()


def get_all_virtualdirectory():
    return list(vdircollection.find({}, {'_id': False}))


def get_virtualdirectory_by_name(name):
    myquery = {"_id": name}

    vdir = vdircollection.find(myquery)
    profile = []
    for x in vdir:
        profile.append(x)

    return profile

# save_file_to_db('AWS', '/home/richa/Documents/MapReduce.docx', 'MapReduce.docx', 'richa')

# add_user_for_file('richa', 'test123')

# profile = get_profile_by_uuid('11111')
# print(profile)

# profile = Profile('11111',
#                   'richa.rastogi',
#                   'test',
#                   'test',
#                   'test',
#                   'test',
#                   'test',
#                   'richa',
#                   'rastogi',
#                   'test',
#                   'rrastogi@iu.edu')

# save_user_to_db(profile)

# save_vdir_to_db('test', 'test description', 'local', '/home/richa/test')

# list = get_all_virtualdirectory()
# for x in list:
#   print(x)


# print(get_virtualdirectory_by_name('test'))
