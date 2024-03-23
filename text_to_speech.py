# import pyttsx3
import pandas as pd
import praw
from praw.models import MoreComments
import re
from gtts import gTTS


def read(post):
    # engine = pyttsx3.init()
    # engine = pyttsx3.init(driverName=None, debug=True)
    # engine.save_to_file(post , 'output.mp3')
    # print("hello")
    # engine.say("I will speak this text")
    # engine.runAndWait()
    tts = gTTS(post)
    tts.save('test.mp3')

    
   

# # link = input("Enter the reddit post URL: ")
# # readComments(link)


# read("this should work")


import pandas as pd
import praw
from praw.models import MoreComments

def readComments(url):
    
    #reddit = praw.Reddit(client_id="client_id",client_secret="client_secret",password="password",user_agent="user_agent",username="username",)
    reddit = praw.Reddit(
        client_id="p-0Rg9Wj6VPI3d-VTepKaw",
        password = 'qcshH3akuFv@yVbx', 
        client_secret="NXrxt3AzjouqlVVG6keHxaVJyBJ1dQ",
        redirect_uri="http://localhost:8080",
        user_agent="amelia2004w",
    )

    submission = reddit.submission(url = url)
    posts = []
    for top_level_comment in submission.comments[1:]:
        if isinstance(top_level_comment, MoreComments):
            continue
        posts.append(top_level_comment.body)
    posts = pd.DataFrame(posts,columns=["body"])  
    indexNames = posts[(posts.body == '[removed]') | (posts.body == '[deleted]')].index
    posts.drop(indexNames, inplace=True)
    # print(posts)
    str = ""
    for i in posts.index:
        str += posts['body'][i]
    str = re.sub(r'[^A-Za-z0-9 ]+', '', str)
    print(posts['body'][0])
    print(submission)
    # read(str)
    

link = input("Enter the reddit post URL: ")
readComments(link)