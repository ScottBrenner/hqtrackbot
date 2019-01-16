from urllib.parse import quote_plus
from urlmatch import urlmatch
import re
import argparse
import youtube
import praw
import os
import time
from datetime import datetime
import plotly
import plotly.graph_objs as go

START_TIME = time.time()
REPLY_TEMPLATE = """[I found a higher-quality upload of this track!](https://www.youtube.com/watch?v={})

----

^^Incorrect? ^^Comments ^^with ^^score ^^below ^^0 ^^will ^^be ^^deleted ^^| ^[^Source](https://github.com/ScottBrenner/hqtrackbot) ^^| [^^Add ^^me ^^to ^^a ^^subreddit!](https://www.reddit.com/message/compose?to=Scottstimo&subject=hqtrackbot&message=)"""

def main():
    reddit = praw.Reddit(user_agent='hqtrackbot (by /u/scottstimo)',
                         client_id=os.environ['REDDIT_CLIENT_ID'], client_secret=os.environ['REDDIT_CLIENT_SECRET'],
                         username=os.environ['REDDIT_USERNAME'], password=os.environ['REDDIT_PASSWORD'])

    subreddit = reddit.subreddit(os.environ['REDDIT_SUBREDDITS'])
    for submission in subreddit.stream.submissions():
        if submission.created_utc < START_TIME:
            continue
        process_submission(submission)
        # Plotly graphing: https://plot.ly/~ScottBrenner/17
        now = datetime.now()
        plotly.tools.set_credentials_file(username=os.environ['PLOTLY_USERNAME'], api_key=os.environ['PLOTLY_API_KEY'])
        fig = plotly.plotly.get_figure("https://plot.ly/~ScottBrenner/17")
        if now.strftime("%Y-%m-%d") not in fig['data'][0]['x']:
            data = [go.Bar(x=[now.strftime("%Y-%m-%d")], y=[1])]
        else:
            data = [go.Bar(x=[now.strftime("%Y-%m-%d")], y=[fig['data'][0]['y'][-1]+1])]
        plotly.plotly.plot(data, filename='hqtrackbot', fileopt='extend')


def process_submission(submission):
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
        if (url_title in submission.url):
            return
        print('Replying to: {}'.format(submission.permalink))
        submission.reply(reply_text)    


if __name__ == '__main__':
    main()
