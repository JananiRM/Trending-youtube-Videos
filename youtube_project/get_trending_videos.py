from googleapiclient.discovery import build

# Replace 'YOUR_API_KEY' with your actual API key
api_key = 'AIzaSyB3idta-x8Z1IDVZhZXjd542e0UEkDlYPc'

def get_trending_videos():
    youtube = build('youtube', 'v3', developerKey=api_key)

    request = youtube.videos().list(
        part='snippet,contentDetails,statistics',
        chart='mostPopular',
        regionCode='IN',
        maxResults=10
    )
    
    response = request.execute()

    return response

if __name__ == "__main__":
    trending_videos = get_trending_videos()
    for video in trending_videos['items']:
        print(f"Title: {video['snippet']['title']}")
        print(f"Description: {video['snippet']['description']}")
        print(f"Channel: {video['snippet']['channelTitle']}")
        print(f"Views: {video['statistics']['viewCount']}")
        print("-----------")
