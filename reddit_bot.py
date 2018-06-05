import praw
import config#bot as config
import pprint as p
import time
import os
import argparse
import urllib.request

def bot_login():
    r = praw.Reddit(client_id = config.client_id, 
                    client_secret = config.client_secret,
                    password = config.password,
                    username = config.username,
                    user_agent = "Sam Test Bot" )
    print("Logged in as {}!".format(config.username))
    return r


def run_bot(r):#, subreddit,comments_on_off, post_limit = 10):
    subreddit = r.subreddit("dankmemes")
    subType = subreddit.hot(limit = 5)
    #subreddit.unsubscribe()
    for submission in subType:
        if not submission.stickied:
            print("Title: {}, ups: {}, Have you visited: {}\nURL: {} \t ID:{}"
            .format( submission.title, submission.ups, submission.visited, submission.url, submission.id))
"""
            submission.comments.replace_more(limit = 0)
            submission.comments_sort = "top"

            for comment in submission.comments:
                commentInfo = "{}  [ {} ]".format(comment.author, comment.score)
                commentBody = "{}".format(comment.body.strip())

                print("\n" + (len(commentInfo)*"_") + "\n")
                print("{}\n{}".format(commentInfo, commentBody))

                comment.replies.replace_more(limit = 0)
                comment_replies(comment, 5)
                print(((len(commentBody) if len(commentBody) <= 50 else 50 )*"-"))
"""
                    
                    
        
def comment_replies(c,limit,  n = 1):
    if len(c.replies) > 0 and n <= limit:
        for r in c.replies:
            print("{}> {} [ {} ]\n{} {}".format(n*'---', r.author, r.score, n* '   ', r.body.strip()))
            time.sleep(1)
            comment_replies(r, limit, n+1)

def stream(r, subreddit, comments_replied_to):
    subreddit = r.subreddit(subreddit)
    print("Streaming comments form {}!".format(subreddit))
    for comment in subreddit.stream.comments():
    #for submission in subreddit.stream.submissions():
        try:
            if comment.author in ("AutoModerator", "KeepingDankMemesDank"):
                print("\n{0}\nSkipped {1} Post\n{0}\n".format(10*"*", comment.author))
                continue
            print("\n{}: {}\nSubmission ID: {}\n{}".format(comment.author, comment.body, comment.submission, time.ctime()))#title)
            #submission_to_save = r.submission(id=comment.submission)
            #print(submission_to_save.title)
            #if "!save" == comment.body:
            if "!save" == comment.body and comment.id not in comments_replied_to: #and comment.author == "Lord_P155taker":
                print("{}".format(20*"-"))
                
                sub_save = r.submission(id=comment.submission)
                url = sub_save.url
                path = "C:\\Users\\user\\Desktop\\Reddit\\{}\\".format(subreddit)
                if not os.path.exists(path):
                    os.makedirs(path)
                name = sub_save.title.lower().strip().replace(" ", "_")
                name = ''.join(e for e in sub_save.title.lower().strip().replace(" ", "_") if (e.isalnum() or e == '_' or e =='-'))
                file_type = url[-3:] 
                
                urllib.request.urlretrieve(url, "{}{}.{}".format(path, name, file_type))
                comment.delete()
                print("Saved Post to {}{}.{}".format(path, name, file_type))
                comments_replied_to.append(comment.id)
                with open("comments_replied_to.txt", "a") as f:
                    f.write("{}\n".format(comment.id))
                print("Saved comment Id")
                print("{}".format(20*"-"))
                time.sleep(6)


        except Exception as e:
            print("AN ERROR OCCURRED: {}".format(str(e)))

def get_saved_comments():
    if not os.path.isfile("comments_replied_to.txt"):
        comments_replied_to = []
    else:
        with open("comments_replied_to.txt", "r") as f:
            comments_replied_to = f.read()
            comments_replied_to = comments_replied_to.split("\n")
    
    return comments_replied_to

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--subreddit", "--s", type=str, default="dankmemes",
                help="Enter the name of the subredfit you want to stream!")
    args = parser.parse_args()

    
    subreddit = args.subreddit.lower().strip().replace(" ", "")
    reddit = bot_login()
    #run_bot(reddit)
    comments_rep_to = get_saved_comments()
    stream(reddit, subreddit, comments_rep_to)
    #reddit.read_only = True
    #submission = reddit.random_subreddit(nsfw=False)
    #p.pprint(vars(submission))
    #run_bot()



if __name__ == '__main__' :
    main()
