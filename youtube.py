#!/usr/bin/python
import argparse
import os
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


DEVELOPER_KEY = os.environ['YOUTUBE_DEVELOPER_KEY']
YOUTUBE_API_SERVICE_NAME = 'youtube'
YOUTUBE_API_VERSION = 'v3'

def youtube_search(options):
  youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
    developerKey=DEVELOPER_KEY)

  # Call the search.list method to retrieve results matching the specified
  # query term.
  search_response = youtube.search().list(
    q=options.q,
    part='id,snippet',
    maxResults=20
).execute()

  # Display the matching videos
  for search_result in search_response.get('items', []):
    if("Provided to YouTube by" in search_result['snippet']['description']):
        return(search_result['id']['videoId'])
   

if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument('--q', help='Search term', default='Google')
  parser.add_argument('--max-results', help='Max results', default=20)
  args = parser.parse_args()

  try:
    youtube_search(args)
  except (HttpError, e):
    print('An HTTP error %d occurred:\n%s' % (e.resp.status, e.content))
