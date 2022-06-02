from googleapiclient.discovery import build
from datetime import datetime
import pandas as pd



youTubeApiKey = '6c265620-c3b7-408f-a76b-6f7e8cdbee30' # Essa é uma chave de API fake.

youtube = build('youtube', 'v3', developerKey=youTubeApiKey)

# Extraindo dados de uma playlist do Youtube
playlistId = 'PLuqj2t1hc3amfYf_s2PuGmy41IOECa6wO'
playlistName = 'Conselhos'

playlist_videos = []
res = youtube.playlistItems().list(part='snippet', playlistId = playlistId, maxResults = 18).execute()

playlist_videos = res['items']

# Extraindo apenas os IDs dos vídeos
videos_ids = list(map(lambda x: x['snippet']['resourceId']['videoId'], playlist_videos))

stats = []

for video_id in videos_ids:
    res = youtube.videos().list(part='statistics', id=video_id).execute()
    stats += res ['items']

# Definindo as dimensões a serem extraídas
videos_titles = list(map(lambda x: x['snippet']['title'], playlist_videos))
video_description = list(map(lambda x: x['snippet']['description'], playlist_videos))
video_id = list(map(lambda x: x['snippet']['resourceId']['videoId'], playlist_videos))

# Definindo os dados a serem extraídos
likes = list(map(lambda x: int(x['statistics']['likeCount']), stats))
views = list(map(lambda x: int(x['statistics']['viewCount']), stats))
comment = list(map(lambda x: int(x['statistics']['commentCount']), stats))

extraction_date = [str(datetime.now())]*len(videos_ids)

# Criando um DataFrame com Pandas
playlist_df = pd.DataFrame({
    'title': videos_titles,
    'video_id': video_id,
    'likes': likes,
    'views': views,
    'comment': comment,
})
print(playlist_df.head())