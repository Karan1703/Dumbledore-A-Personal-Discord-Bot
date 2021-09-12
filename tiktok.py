from TikTokApi import TikTokApi
import random
import string 
api = TikTokApi()
def get_url():
  starter = 'willsmith'
  custom_did = ''.join(random.choice(string.digits) for num in range(19))
  tiktokid = api.getUser(starter)["userInfo"]['user']['id']

  suggested_users = [api.getSuggestedUsersbyIDCrawler(count=10, startingId=tiktokid)]

  rand_user = api.getUser(random.choice(suggested_users))

  rand_vids = api.byUsername(rand_user['user'], count = 10)

  vid = random.choice(rand_vids)
  vid_url = vid['video']['downloadAddr']

  vid = api.get_Video_By_DownloadURL(vid_url, custom_did = custom_did)
  with open("vid.mp4", 'wb') as o:
    o.write(vid)


  