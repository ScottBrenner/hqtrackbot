# hqtrackbot
[/u/hqtrackbot](https://old.reddit.com/user/hqtrackbot) - a reddit bot that finds higher-quality YouTube uploads of submitted tracks.

Currently watching subreddits:
https://www.reddit.com/r/Music/wiki/musicsubreddits#wiki_electronic_music

Currently banned from subreddits:
- /r/trance
- /r/listentothis

## Usage
Create and add values:

`docker run -e REDDIT_CLIENT_ID= -e REDDIT_CLIENT_SECRET= -e REDDIT_USERNAME= -e REDDIT_PASSWORD= -e REDDIT_SUBREDDITS= -e YOUTUBE_DEVELOPER_KEY=
 scottbrenner/hqtrackbot:latest`
