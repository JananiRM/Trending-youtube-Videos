from flask import Flask, render_template, jsonify, request
from googleapiclient.discovery import build
from country_codes import country_codes  # Import the country code mapping

app = Flask(__name__)

# Replace 'YOUR_API_KEY' with your actual API key
api_key = 'AIzaSyB3idta-x8Z1IDVZhZXjd542e0UEkDlYPc'

def get_trending_videos(region_code='IN'):
    youtube = build('youtube', 'v3', developerKey=api_key)

    request = youtube.videos().list(
        part='snippet,contentDetails,statistics',
        chart='mostPopular',
        regionCode=region_code,
        maxResults=10
    )

    response = request.execute()
    videos = []
    for item in response['items']:
        video_data = {
            'id': item['id'],
            'snippet': {
                'title': item['snippet']['title'],
                'description': item['snippet']['description'],
                'channelTitle': item['snippet']['channelTitle'],
                'publishedAt': item['snippet']['publishedAt']
            },
            'statistics': {
                'viewCount': item['statistics']['viewCount'],
                'likeCount': item['statistics'].get('likeCount', 0),
                'dislikeCount': item['statistics'].get('dislikeCount', 0),
                'commentCount': item['statistics'].get('commentCount', 0),
            },
            'contentDetails': {
                'duration': item['contentDetails']['duration']
            }
        }
        videos.append(video_data)
    return videos

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_videos')
def get_videos():
    country_name = request.args.get('country_name', 'India')
    region_code = country_codes.get(country_name, 'IN')  # Default to India if country not found
    videos = get_trending_videos(region_code)
    return jsonify(videos)

@app.route('/get_video_details/<video_id>')
def get_video_details(video_id):
    youtube = build('youtube', 'v3', developerKey=api_key)
    
    request = youtube.videos().list(
        part='snippet,contentDetails,statistics',
        id=video_id
    )
    
    response = request.execute()
    return jsonify(response['items'][0])

if __name__ == '__main__':
    app.run(debug=True)

