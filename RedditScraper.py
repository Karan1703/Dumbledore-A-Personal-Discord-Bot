import praw


reddit = praw.Reddit(client_id = "rU6g17f_4AkaRQ", client_secret = "hauOsakNbPJIGghgWuKmlESjRUWe9Q", username ="chimera1703  ", password ="karan231", user_agent = "redditscraper")

subreddit = reddit.subreddit("harrypottermemes")

top_memes = subreddit.top("month")
