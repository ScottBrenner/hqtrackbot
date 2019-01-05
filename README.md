# hqtrackbot
[/u/hqtrackbot](https://old.reddit.com/user/hqtrackbot) - a reddit bot that finds higher-quality versions of submitted tracks.

## Usage
`docker build . -t hqtrackbot`

Create and add keys:

`docker run -e REDDIT_CLIENT_ID= -e REDDIT_CLIENT_SECRET= -e REDDIT_USERNAME= -e REDDIT_PASSWORD= -e REDDIT_SUBREDDITS= -e YOUTUBE_DEVELOPER_KEY=
 hqtrackbot`
