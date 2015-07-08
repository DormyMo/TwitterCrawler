#coding:utf8
__author__ = 'modm'

class UserItem():
    '''
    :key: user_id,nick_name,head_img,screen_name,desc,location,site,join_date,tweets,following,followers,favorites,lists,isVerified
    '''
    def __init__(self):
        self._values={"user_id":"",
                      "nick_name":"",
                      "head_img":"",
                      "screen_name":"",
                      "desc":"",
                      "location":"",
                      "site":"",
                      "join_date":"",
                      'tweets':"",
                      'following':0,
                      'followers':0,
                      'favorites':0,
                      'lists':0,
                      "isVerified":False}
    def __getitem__(self, item):
        if item in self._values.keys():return self._values[item]
        else:raise KeyError("%s does not support field: %s" %(self.__class__.__name__, item))
    def __setitem__(self, key, value):
        if self._values.has_key(key):self._values[key]=value
        else:raise KeyError("%s does not support field: %s" %(self.__class__.__name__, key))
    def __str__(self):
        return str(self._values)
    def __len__(self):
        return len(self._values)
    def keys(self):
        return self._values.keys()
class TimelineItem():
    '''
    :key: screen_name,itemId,timestamp,textStr,links,imgs,ats,retweet,favorite,retweetFromScreenName,retweetFromUserId,retweetId,isRetweet
    '''
    def __init__(self):
        self._values={'screen_name':"",
                      "user_id":"",
                      "itemId":"",
                      "timestamp":"",
                      "texts":"",
                      "links":[],
                      "imgs":[],
                      'ats':[],
                      "retweet":0,
                      "favorite":0,
                      'retweetFromScreenName':"",
                      'retweetFromUserId':"",
                      'retweetId':"",
                      'isRetweet':False}
    def __getitem__(self, item):
        if item in self._values.keys():return self._values[item]
        else:raise KeyError("%s does not support field: %s" %(self.__class__.__name__, item))
    def __setitem__(self, key, value):
        if self._values.has_key(key):self._values[key]=value
        else:raise KeyError("%s does not support field: %s" %(self.__class__.__name__, key))
    def __str__(self):
        return str(self._values)
    def __len__(self):
        return len(self._values)
    def keys(self):
        return self._values.keys()
if __name__=="__main__":
    user = UserItem()
    for key in user.keys():
        print key,user[key]
    user['user_id']=1
    print user
    print len(user)
