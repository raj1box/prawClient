import praw
import pandas as pd
import sys

comments = {"sub id": [],
            "comment": []}


def main():
    search_key_word = []
    if (len(sys.argv) > 1):
        search_key_word = sys.argv[1:]
    else:
        print("No keywords found in CLA.Program exiting")
        exit()
    reddit = praw.Reddit("DEFAULT", user_agent="prawClient u/{username}")
    print("logged in user : " + reddit.user.me().name)
    for key in search_key_word:
        print("Starting subreddit call for keyword : " + key)
        comments["sub id"].clear()
        comments["comment"].clear()
        subreddit = reddit.subreddit(key)
        hot_data = subreddit.hot(limit=None)
        hot_df = extract_data(hot_data)
        rising_data = subreddit.rising(limit=None)
        rising_df = extract_data(rising_data)
        new_data = subreddit.new(limit=None)
        new_df = extract_data(new_data)
        frames = [hot_df, rising_df, new_df]
        result = pd.concat(frames, ignore_index=True)
        result.to_csv(key + "_results.csv")
        comments_df = pd.DataFrame(comments)
        comments_df.to_csv(key+"_comments.csv")

def extract_data(data):
    data_dict = {"sub id": [],
                 "title": [],
                 "subreddit": [],
                 "total comments": [],
                 "text": []}
    for submission in data:
        sub_id=submission.id
        data_dict["sub id"].append(sub_id)
        data_dict["title"].append(submission.title)
        data_dict["subreddit"].append(submission.subreddit)
        data_dict["total comments"].append(submission.num_comments)
        data_dict["text"].append(submission.selftext)
        submission.comments.replace_more(limit=None)
        for comment in submission.comments.list():
            comments["sub id"].append(sub_id)
            comments["comment"].append(comment)
    df = pd.DataFrame(data_dict)
    return df
    # df.to_csv(key + "_results.csv")


main()
