from urllib.parse import quote_plus
from urlmatch import urlmatch
import re
import argparse
import youtube
import praw
import os

REPLY_TEMPLATE = """[I found a higher-quality version of this track!](https://www.youtube.com/watch?v={})

----

^^I ^^am ^^a ^^bot ^^and ^^this ^^action ^^was ^^performed ^^automatically ^^| ^[^Source](https://github.com/ScottBrenner/hqtrackbot) ^^| [^^Add ^^to ^^your ^^subreddit](https://www.reddit.com/message/compose?to=Scottstimo&subject=hqtrackbot&message=)"""

def main():
    reddit = praw.Reddit(user_agent='hqtrackbot (by /u/scottstimo)',
                         client_id=os.environ['REDDIT_CLIENT_ID'], client_secret=os.environ['REDDIT_CLIENT_SECRET'],
                         username=os.environ['REDDIT_USERNAME'], password=os.environ['REDDIT_PASSWORD'])

    subreddit = reddit.subreddit(os.environ['REDDIT_SUBREDDITS'])
    for submission in subreddit.stream.submissions():
        process_submission(submission)


def process_submission(submission):
    # Ignore submissions that have already been replied to
    submission.comments.replace_more(limit=0)
    for top_level_comment in submission.comments:
        if("I found a higher-quality version of this track!" in top_level_comment.body):
            return
    
    # Ignore non-YouTube submissions (for now)
    youtube_match_pattern = 'https://www.youtube.com/*'    
    youtu_match_pattern = 'https://youtu.be/*'

    if (urlmatch(youtube_match_pattern, submission.url) == False and urlmatch(youtu_match_pattern, submission.url) == False):
        return

    parser = argparse.ArgumentParser()
    parser.add_argument('--q', help='Search term', default=re.sub(r'([\[]).*?([\]])', '', submission.title))
    parser.add_argument('--max-results', help='Max results', default=10)
    args = parser.parse_args()
    if(youtube.youtube_search(args)):
        url_title = quote_plus(youtube.youtube_search(args))
        reply_text = REPLY_TEMPLATE.format(url_title)
        if (submission.url in reply_text):
            return
        print('Replying to: {}'.format(submission.permalink))
        print(reply_text)
        submission.reply(reply_text)    


if __name__ == '__main__':
    main()