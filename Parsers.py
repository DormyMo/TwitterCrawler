#coding:utf8
__author__ = 'modm'
from lxml import  etree
from Utils import getFirstItem
from Items import UserItem,TimelineItem
import sys
import datetime
import urllib2
def _parseDate(date):
    dateStr=''
    if date:
        if date.encode('utf8').find('年')>-1:
            join_date=date.encode('utf8').replace('上午','AM ').replace('下午','PM ').replace('下午','PM').replace('年',' ').replace('月',' ').replace('日','')
            join_date=datetime.datetime.strptime(join_date,'%p %I:%M - %Y %m %d')
        else:
            join_date=datetime.datetime.strptime(date,'%I:%M %p - %d %b %Y');
        dateStr = join_date.strftime('%Y-%m-%d %H:%M')
        return  dateStr
def _parseNumStr2Int(numStr):
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
def userInfoParser(html,flag=""):
    '''
    :param html:
    :param flag:
    :return: UserItem()
    '''
    user=UserItem()
    try:
        print 'getUserInfo gen etree ing ...',flag
        tree = etree.HTML(html)
        print 'getUserInfo gen etree done ...',flag
        screen_name=getFirstItem(tree.xpath('//*[@class="ProfileHeaderCard"]/h2[1]/a/span/text()'))
        head_img=getFirstItem(tree.xpath('//*[@class="ProfileAvatar-container u-block js-tooltip profile-picture media-thumbnail"]/@href'))
        user_id =getFirstItem(tree.xpath('//*[@class="ProfileNav"]/@data-user-id'))
        div = getFirstItem(tree.xpath('//*[@class="ProfileHeaderCard"]'))
        nick_name = getFirstItem(div.xpath('*[@class="ProfileHeaderCard-name"]/a/text()'))
        isVerified = div.xpath('*[@class="ProfileHeaderCard-name"]/span')>0
        screen_name=getFirstItem(div.xpath('*[@class="ProfileHeaderCard-screenname u-inlineBlock u-dir"]/a/span/text()'))
        desc=getFirstItem(div.xpath('*[@class="ProfileHeaderCard-bio u-dir"]/a/text() | *[@class="ProfileHeaderCard-bio u-dir"]/text()'))
        location = getFirstItem(div.xpath('*[@class="ProfileHeaderCard-location"]/span[@class="ProfileHeaderCard-locationText u-dir"]/text()'))
        location= location.replace('\n','').replace(' ','') if location else None
        site = getFirstItem(div.xpath('*[@class="ProfileHeaderCard-url "]/span[@class="ProfileHeaderCard-urlText u-dir"]/a/@title'))
        join_date = getFirstItem(div.xpath('*[@class="ProfileHeaderCard-joinDate"]/span[@class="ProfileHeaderCard-joinDateText js-tooltip u-dir"]/@title | *[@class="ProfileHeaderCard-joinDate"]/span[@class="ProfileHeaderCard-joinDateText js-tooltip u-dir"]/@title'))
        join_date = _parseDate(join_date)
        div2 = getFirstItem(tree.xpath('//*[@class="ProfileNav-list"]'))
        tweets  = _parseNumStr2Int(getFirstItem(div2.xpath('li[@class="ProfileNav-item ProfileNav-item--tweets is-active"]/a/span[2]/text()')))
        following = _parseNumStr2Int(getFirstItem(div2.xpath('li[@class="ProfileNav-item ProfileNav-item--following"]/a/span[2]/text()')))
        followers = _parseNumStr2Int(getFirstItem(div2.xpath('li[@class="ProfileNav-item ProfileNav-item--followers"]/a/span[2]/text()')))
        favorites = _parseNumStr2Int(getFirstItem(div2.xpath('li[@class="ProfileNav-item ProfileNav-item--favorites"]/a/span[2]/text()')))
        lists     = _parseNumStr2Int(getFirstItem(div2.xpath('li[@class="ProfileNav-item ProfileNav-item--lists"]/a/span[2]/text()')))

        user["user_id"]=user_id
        user["nick_name"]=nick_name
        user["head_img"]=head_img
        user["screen_name"]=screen_name
        user["desc"]=desc
        user["location"]=location
        user["site"]=site
        user["join_date"]=join_date
        user['tweets']=tweets
        user['following']=following
        user['followers']=followers
        user['favorites']=favorites
        user['lists']=lists
        user["isVerified"]=isVerified
    except Exception,e:
        print sys.stderr.write(str(e))
        raise Exception("parse user err",e)
    #return  {"user_id":user_id,"nick_name":nick_name,"head_img":head_img,"screen_name":screen_name,"desc":desc,"location":location,"site":site,"join_date":join_date,'tweets':tweets,'following':following,'followers':followers,'favorites':favorites,'lists':lists,"isVerified":isVerified}
    return user
def followParser(html,flag=""):
    '''
    :param html:
    :param flag:
    :return: UserItem() generator
    '''
    try:
        tree = etree.HTML(html)
        itemDivs = tree.xpath('//*[@class="ProfileCard js-actionable-user"]')
        for itemDiv in itemDivs:
            user = UserItem()
            user_id=itemDiv.xpath('@data-user-id')
            screen_name=itemDiv.xpath('@data-screen-name')
            nick_name=itemDiv.xpath('*[@class="ProfileCard-content"]/a/@title')
            head_img=itemDiv.xpath('*[@class="ProfileCard-content"]/a/img/@src')
            desc=itemDiv.xpath('*[@class="ProfileCard-content"]/*[@class="ProfileCard-userFields"]/p[@class="ProfileCard-bio u-dir js-ellipsis"]/text()')
            if not desc:
                desc=itemDiv.xpath('*[@class="ProfileCard-content"]/*[@class="ProfileCard-userFields"]/p[@class="ProfileCard-bio u-dir"]/text()')
            user_id=getFirstItem(user_id)
            screen_name=getFirstItem(screen_name)
            nick_name=getFirstItem(nick_name)
            head_img=getFirstItem(head_img)
            desc=getFirstItem(desc)
            isVerified = len(itemDiv.xpath('*[@class="ProfileCard-content"]/*[@class="ProfileCard-userFields"]/div/div/div/a/span'))>0
            #yield {'cursor':res['cursor'],'user_id':user_id,"screen_name":screen_name,"nick_name":nick_name,"head_img":head_img,"desc":desc}
            user["user_id"]=user_id,
            user["nick_name"]=nick_name,
            user["head_img"]=head_img,
            user["screen_name"]=screen_name,
            user["desc"]=desc,
            user["location"]="",
            user["site"]="",
            user["join_date"]="",
            user['tweets']="",
            user['following']=0,
            user['followers']=0,
            user['favorites']=0,
            user['lists']=0,
            user["isVerified"]=isVerified
            #users.append(user)
            yield  user
    except Exception,e:
        print sys.stderr.write('getFollowers ParseError ,break... cursor '+flag+str(e))
        yield []
def timelineParser(html,flag=""):
    '''

    :param html:
    :param flag:
    :return: TimelineItem() generator
    '''
    try:
        tree = etree.HTML(html)
        divs=None
        while not divs:divs = tree.xpath('//*[@class="Grid"]/div/*[@class="StreamItem js-stream-item"]') or tree.xpath('//*[@class="js-stream-item stream-item stream-item expanding-stream-item\n"]')
        for div in divs:
            timelineObj=TimelineItem()
            itemId = getFirstItem(div.xpath('@data-item-id'))
            #header=getFirstItem(div.xpath('div/div[@class="ProfileTweet-header u-cf"]')) or getFirstItem(div.xpath('div/div[@class="ProfileTweet-header u-cf"]'))
            contents = getFirstItem(div.xpath('div/div[@class="ProfileTweet-contents"]')) or getFirstItem(div.xpath('div/div[@class="content"]'))
            timestamp = getFirstItem(div.xpath('div/div[@class="ProfileTweet-header u-cf"]/div/span/a/span/@data-time')) or getFirstItem(div.xpath('//*[@class="js-stream-item stream-item stream-item expanding-stream-item\n"]/div/div[@class="content"]/div[@class="stream-item-header"]/small/a/span/@data-time'))
            retweetFromScreenName=''
            retweetFromUserId=''
            retweetId=''
            retweetStr = getFirstItem(div.xpath('div/div[@class="ProfileTweet-header u-cf"]/span/a[@class="ProfileTweet-actionButton js-nav js-permalink"]/@href'))
            #if retweetStr:
                #retweetStrs = retweetStr.split('/')
                #retweetFromScreenName = retweetStrs[1]
                #retweetId = retweetStrs[3]
            retweetFromScreenName= getFirstItem(div.xpath('div[1]/@data-screen-name')) or ''
            retweetFromUserId = getFirstItem(div.xpath('div[1]/@data-user-id')) or ''
            retweetId = getFirstItem(div.xpath('div[1]/@data-retweet-id')) or ''
            texts = contents.xpath('p/text()')
            links = contents.xpath('p//a/@href')
            group = getFirstItem(contents.xpath('div[@class="ProfileTweet-actionList u-cf js-actions"]')) or getFirstItem(contents.xpath('div/div[@role="group"]'))
            if group:
                #reply = getFirstItem(group.xpath('div[1]/button[1]/span[@class="ProfileTweet-actionCount"]/span/text()'))
                retweet =  _parseNumStr2Int(getFirstItem(group.xpath('div[2]/button[1]/span[@class="ProfileTweet-actionCount"]/span/text()'))) or 0
                favorite = _parseNumStr2Int(getFirstItem(group.xpath('div[3]/button[1]/span[@class="ProfileTweet-actionCount"]/span/text()'))) or 0
            else:
                reply=0
                retweet=0
                favorite=0
            textStr=""
            for i in range(len(texts)):
                if i<=len(links)-1:
                    linkStr = links[i]
                    if links[i].find('/hashtag') >-1 :
                        linkStr = '#'+urllib2.unquote(links[i].replace('?src=hash','').split('/')[2].encode('utf8'))
                        linkStr = linkStr.decode('utf8')
                    if links[i][0]=='/':
                        linkStr = linkStr.replace('/','@')

                    textStr+=texts[i]+' '+linkStr
                else:
                    textStr+=texts[i]
            texts=textStr
            imgs = contents.xpath('div/div/div/div/a/img/@src |div/div/div/div/div/div//div/img/@src')
            ats = [link[1:] for link in links if link[0]=='/' and link[0:8]!='hashtag/']
            links = [link for link in links if link[0]!='/' and link[0:8]!='/hashtag']
            isRetweet = True if  retweetId else False


            timelineObj['screen_name']=''
            timelineObj['user_id']=''
            timelineObj['itemId']=itemId
            timelineObj['timestamp']=timestamp
            timelineObj['texts']=texts
            timelineObj['links']=links
            timelineObj['imgs']=imgs
            timelineObj['ats']=ats
            timelineObj['retweet']=retweet
            timelineObj['favorite']=favorite
            timelineObj['retweetFromScreenName']=retweetFromScreenName
            timelineObj['retweetFromUserId']=retweetFromUserId
            timelineObj['retweetId']=retweetId
            timelineObj['isRetweet']=isRetweet
            yield timelineObj
    except Exception,e:
        print  sys.stderr.write('html extract err : '+str(e)+'\n')
        print sys.stderr.write('getFollowers ParseError ,break...'+flag+str(e))
        yield []
