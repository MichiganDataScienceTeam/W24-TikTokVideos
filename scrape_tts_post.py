
import praw
import pandas as pd
import re
from gtts import gTTS
from cleantext import clean


def read(post, index):
    tts = gTTS(post)
    tts.save('test' + str(index) + '.mp3')

def read_post():

    reddit_read_only = praw.Reddit(
            client_id="p-0Rg9Wj6VPI3d-VTepKaw",
            password = 'qcshH3akuFv@yVbx', 
            client_secret="NXrxt3AzjouqlVVG6keHxaVJyBJ1dQ",
            redirect_uri="http://localhost:8080",
            user_agent="amelia2004w",
        )
    
    
    subreddit = reddit_read_only.subreddit("AITAH")
    
    # Display the name of the Subreddit
    print("Display Name:", subreddit.display_name)
    
    # Display the title of the Subreddit
    print("Title:", subreddit.title)
    
    # Display the description of the Subreddit
    print("Description:", subreddit.description)

    posts = subreddit.top()
    # Scraping the top posts of the current month
    
    posts_dict = {"Title": [], "Post Text": [],
                "ID": [], "Score": [],
                "Total Comments": [], "Post URL": []
                }
    
    for post in posts:
        # Title of each post
        posts_dict["Title"].append(post.title)
        
        # Text inside a post
        posts_dict["Post Text"].append(post.selftext)
        
        # Unique ID of each post
        posts_dict["ID"].append(post.id)
        
        # The score of a post
        posts_dict["Score"].append(post.score)
        
        # Total number of comments inside the post
        posts_dict["Total Comments"].append(post.num_comments)
        
        # URL of each post
        posts_dict["Post URL"].append(post.url)
    
    # Saving the data in a pandas dataframe
    top_posts = pd.DataFrame(posts_dict)

    # read the first _ posts from top_posts and save into separate mp3's
    for i in range(3):
        str = clean(top_posts["Post Text"][i], no_emoji = True)
        # print(str)
        read(str, i)


read_post()
