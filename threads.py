#coding:utf8
__author__ = 'modm'
import threading
from Spiders import TwitterSpider
class CrawlUserInfoThread(threading.Thread):
    def __init__(self,threadName):
        threading.Thread.__init__(self);
        self.thredName = 'crawlUserInfoThread : '+str(threadName)
        self.ts = TwitterSpider()
    def run(self):
        user= self.ts.getUserInfo("dormymo")
        print user
class CrawlTimelineThread(threading.Thread):
    def __init__(self,threadName):
        threading.Thread.__init__(self);
        self.thredName = 'CrawlTimelineThread : '+str(threadName)
        self.ts = TwitterSpider()
    def run(self):
        for timeline in self.ts.getTimeline("dormymo"):
            print timeline
class CrawlFollowersThread(threading.Thread):
    def __init__(self,threadName):
        threading.Thread.__init__(self);
        self.thredName = 'CrawlFollowersThread : '+str(threadName)
        self.ts = TwitterSpider()
    def run(self):
        for user in self.ts.getFollowersUsers("dormymo"):
            print user
class CrawlFollowingThread(threading.Thread):
    def __init__(self,threadName):
        threading.Thread.__init__(self);
        self.thredName = 'CrawlFollowingThread : '+str(threadName)
        self.ts = TwitterSpider()
    def run(self):
        for user in self.ts.getFollowingUsers("dormymo"):
            print user
if __name__=='__main__':
    # CrawlUserInfoThread(1).start()
    # CrawlTimelineThread(1).start()
    # CrawlFollowersThread(1).start()
    CrawlFollowingThread(1).start()