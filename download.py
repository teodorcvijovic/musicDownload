from tokenize import String

import youtube_dl
import urllib.request
import re

KEYWORDS_FILE = 'keywords.txt'
RESULT_NUM = 0  # get first result
useURLs = False  # KEYWORDS_FILE contains URLs, not keywords

def findVideoURL(keyword: String):
    if useURLs:
        return keyword
    searchKeyword = keyword.replace(' ', '+')[:-1]
    html = urllib.request.urlopen("https://www.youtube.com/results?search_query=" + searchKeyword)
    videoId = re.findall(r"watch\?v=(\S{11})", html.read().decode())[RESULT_NUM]
    videoURL = "https://www.youtube.com/watch?v=" + videoId
    return videoURL

def searchAndDownload(keyword):
    videoURL = findVideoURL(keyword)
    videoInfo = youtube_dl.YoutubeDL().extract_info(
        url=videoURL, download=False
    )
    filename = f"downloaded/{videoInfo['title']}.mp3"
    options = {
        'format': 'bestaudio/best',
        'keepvideo': False,
        'outtmpl': filename,
    }

    with youtube_dl.YoutubeDL(options) as ydl:
        ydl.download([videoInfo['webpage_url']])

    print("Download complete: {}".format(filename))

def run():
    with open(KEYWORDS_FILE, 'r') as file:
        for keyword in file:
            try:
                searchAndDownload(keyword)
            except Exception:
                print('Error: Video ' + keyword + ' failed to download.')

if __name__ == '__main__':
    run()
