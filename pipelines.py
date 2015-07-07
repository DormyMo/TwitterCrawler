#coding:utf8
__author__ = 'modm'
from pymongo import MongoClient,errors,DESCENDING
import datetime
import hashlib
import datetime
class SingleMongodbPipeline(object):
    def __init__(self,db_name,collection_name):
        self.client = MongoClient('mongodb://127.0.0.1:27017/')
        self.db = self.client[db_name]
        self.posts = self.db[collection_name]
    def storeContent(self,content):
        content['created_time']=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        try:
            post_id = self.posts.insert(content)
            print 'store 2 mongo :',post_id
        except errors.DuplicateKeyError,e:
            raise Exception('err','DuplicateKeyError')
    def findOne(self,conditionDict):
        return self.posts.find_one(conditionDict)
    def findOneBySort(self,conditionDict,sortDict):
        collections =  self.posts.find(conditionDict).sort([('rank',DESCENDING)])
        return collections[0] if collections else None
    def findAll(self,conditionDict):
        for post in  self.posts.find(conditionDict).batch_size(30):
            yield post
    def findAndUpdate(self,queryDict,updateDict,sort=None):
        if sort:
            return self.posts.find_and_modify(query=queryDict, update={"$set": updateDict},sort=sort,upsert=False, full_response= True)['value']
        else:
            return self.posts.find_and_modify(query=queryDict, update={"$set": updateDict}, upsert=False, full_response= True)['value']
    def updateContent(self,conditionDict,setsDicts):
        self.posts.update(conditionDict,{"$set":setsDicts},upsert=False)
    def close(self):
        self.db.close()
        self.posts.close()