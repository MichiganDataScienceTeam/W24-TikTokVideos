import praw

# Reddit API credentials
client_id = 'TemDBAv4OB3tpA9vMqf5ug'
client_secret = 'X1LvL44H3JBbLr5-oXMl_vql5jASOA'
user_agent = 'Ray/1.0 by /u/LMVJ-RAY'

# Create a Reddit instance
reddit = praw.Reddit(client_id=client_id,
                     client_secret=client_secret,
                     user_agent=user_agent)

# Subreddit name from which you want to download posts
subreddit_name = 'WritingPrompts'  # Example: 'WritingPrompts' for story prompts

# Number of posts to download
num_posts = 5

# Get the subreddit instance
subreddit = reddit.subreddit(subreddit_name)

# Get the top posts from the subreddit
top_posts = subreddit.top(limit=num_posts)

# Create a new text file to save the post data
with open('reddit_stories_with_comments.txt', 'w', encoding='utf-8') as file:
    # Write the post data to the text file
    for post in top_posts:
        # Check if the post content is not empty
        if post.selftext.strip():  # Check if the content is not just whitespace
            file.write("Title: " + post.title + "\n")
            file.write("Story: " + post.selftext + "\n")
            file.write("\n")

            # Get the comments of the post
            post.comments.replace_more(limit=None)
            comments = post.comments.list()

            # Write the comments to the file
            for comment in comments:
                file.write("Comment: " + comment.body + "\n")
                file.write("\n")

# Notify the user that the stories and comments have been saved to the file
print("Reddit stories and comments have been saved to reddit_stories_with_comments.txt")