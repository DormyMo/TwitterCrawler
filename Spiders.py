#coding:utf8
__author__ = 'modm'
import time
import sys
from Parsers import userInfoParser,timelineParser,followParser
from Items import UserItem,TimelineItem
from HttpClient import HttpClient
class TwitterSpider():
    def __init__(self):
        self.httpClient = HttpClient()
    def _getUserHomeSiteUrl(self,screen_name):
        return "https://twitter.com/"+screen_name
    def _getFollowersUsersParams(self,cursor):
        return {"max_position": cursor,"include_available_features":1,"include_entities":1}
    def _getFollowersUsersUrl(self,screen_name):
        return 'https://twitter.com/'+screen_name+'/followers/users'
    def _getFollowingUsersParams(self,cursor):
        return {"max_position": cursor,"include_available_features":1,"include_entities":1}
    def _getFollowingUsersUrl(self,screen_name):
        return 'https://twitter.com/'+screen_name+'/following/users'
    def _getTimelineParams(self,max_id=0):
        # params = {"contextual_tweet_id": 261095810454917120,"include_available_features": 1,"include_entities": 1,"last_note_ts": 110,"max_id": 0}
        # if max_id!=0:
        #     params['max_id']=max_id
        #     return params
        params = {"contextual_tweet_id": 261095810454917120,"include_available_features": 1,"include_entities": 1,"last_note_ts": 110,"max_position": 0}
        if max_id!=0:
            params['max_position']=max_id
            return params
    def _getTimelineUrl(self,screen_name):
        return "https://twitter.com/i/profiles/show/"+screen_name+"/timeline"
    def _getUserFromSearchUrl(self,name):
        return "https://twitter.com/search?q="+name+"&mode=users"
    def _getUserFromSearchParam(self,name):
        return {}
    def _parseNumStr2Int(self,numStr):
        if not numStr:
            return 0
        numStr=numStr.replace(',','')
        if numStr.find('K')>-1:
            numStr=numStr.replace('K','')
            return int(float(numStr)*1000)
        elif numStr.find('M')>-1:
            numStr=numStr.replace('M','')
            return int(float(numStr)*1000000)
        elif numStr.find('千'.decode("utf8"))>-1:
            numStr=numStr.replace('千'.decode("utf8"),'')
            return int(float(numStr)*1000)
        elif numStr.find('万'.decode("utf8"))>-1:
            numStr=numStr.replace('万'.decode("utf8"),'')
            return int(float(numStr)*10000)
        else:
            return int(numStr)
    def getFollowersUsers(self,screen_name,cursor=-1):
        cursor=cursor
        while True:
            print 'getFollowersUsers cursor : ',str(cursor)
            try:
                res = self.httpClient.get(self._getFollowersUsersUrl(screen_name), self._getFollowersUsersParams(cursor))
                json = res.json()
                html = json['items_html']
            except ValueError,e:
                print sys.stderr.write('getFollowers ValueError ,break... cursor '+str(cursor)+' screen_name : '+screen_name+"   "+str(e))
                break
            except Exception,e:
                print sys.stderr.write('getFollowers Error ,retry... cursor '+str(cursor)+' screen_name : '+screen_name+"   "+str(e))
                time.sleep(300)
                continue
            for user in followParser(html):
                yield user
            if json['has_more_items']==False or json['min_position']=='0':
                    break
            else:
                cursor=json['min_position']
    def getFollowingUsers(self,screen_name,cursor=-1):
        cursor=cursor
        while True:
            print 'getFollowingUsers cursor : ',str(cursor)
#             waitTime = random.randint(0,3)
#             print 'waitTime : ',waitTime
#             time.sleep(waitTime)
            try:
                res = self.httpClient.get(self._getFollowingUsersUrl(screen_name), self._getFollowingUsersParams(cursor))
                json = res.json()
                html = json['items_html']
            except ValueError,e:
                print sys.stderr.write('getFollowing ValueError ,break... cursor '+str(cursor)+' screen_name : '+screen_name+"   "+str(e))
                break
            except Exception,e:
                print sys.stderr.write('getFollowing Error ,retry... cursor '+str(cursor)+' screen_name : '+screen_name+"   "+str(e))
                time.sleep(300)
                continue
            for user in followParser(html):
                yield user
            if json['has_more_items']==False or json['min_position']=='0':
                    break
            else:
                cursor=json['min_position']
    def getUserInfo(self,screen_name):
        try:
            html = self.httpClient.get(self._getUserHomeSiteUrl(screen_name), {}).content
        except Exception,e:
            print sys.stderr.write('getUserInfo ValueError ,break...   '+str(e))
            return UserItem()
        return userInfoParser(html)
    def getTimeline(self,screen_name):
        max_id=0
        has_more_items=True
        while has_more_items:
            print 'max_id ',max_id
            try:
                res =self.httpClient.get(self._getTimelineUrl(screen_name), self._getTimelineParams(max_id))
                #print res
                #print res.content
                json = res.json()
                html=json['items_html']
                has_more_items=json['has_more_items']
                if not has_more_items:
                    print 'getTimeline no more'
                    break
            except ValueError,e:
                if res.status_code==404:break
                print sys.stderr.write('getTimeline ValueError ,break... max_id '+str(max_id)+str(e))
                time.sleep(30)
                continue
            except Exception,e:
                print sys.stderr.write('getTimeline err ,retry... max_id '+str(max_id)+str(e))
                #raise Exception('timeline net err',e)
                time.sleep(30)
                continue
            for timeline in timelineParser(html):
                max_id = timeline['itemId']
                yield timeline


