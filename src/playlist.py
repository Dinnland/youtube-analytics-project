import os
from datetime import timedelta
from googleapiclient.discovery import build
from src.video import PLVideo


class PlayList:
    """
    класс `PlayList`, который инициализируется _id_ плейлиста
    """
    api_key = os.getenv('YT_API_KEY')
    youtube = build('youtube', 'v3', developerKey=api_key)

    def __init__(self, playlist_id):
        self.playlist_id = playlist_id
        self.playlist_info = self.youtube.playlists().list(part='snippet', id=self.playlist_id).execute()
        self.title = self.playlist_info['items'][0]['snippet']['title']
        self.url = f'https://www.youtube.com/playlist?list={self.playlist_id}'
        self.videos = self.get_videos()

    def get_videos(self):
        """
        Получение списка видео в плейлисте
        """
        videos = []
        pl_info = self.youtube.playlistItems().list(playlistId=self.playlist_id,
                                                    part='snippet',
                                                    maxResults=50
                                                    ).execute()
        for pl_item in pl_info['items']:
            video_id = pl_item['snippet']['resourceId']['videoId']
            videos.append(PLVideo(video_id, self.playlist_id))

        return videos

    @property
    def total_duration(self):
        """
        возвращает объект класса `datetime.timedelta` с суммарной длительность плейлиста
        """
        total_time = timedelta()
        for video in self.videos:
            duration = self.youtube.videos().list(part='contentDetails', id=video.video_id).execute()['items'][0][
                'contentDetails']['duration']
            minutes, seconds = map(int, duration[2:].replace('M', ' ').replace('S', '').split())
            duration = timedelta(minutes=minutes, seconds=seconds)
            total_time += duration
        return total_time

    def show_best_video(self):
        """
        возвращает ссылку на самое популярное видео из плейлиста (по количеству лайков)
        """
        best_video_id = None
        max_likes = 0
        for video in self.videos:
            statistics = self.youtube.videos().list(part='statistics', id=video.video_id).execute()['items'][0][
                'statistics']
            likes = int(statistics['likeCount'])
            if likes > max_likes:
                max_likes = likes
                best_video_id = video.video_id
        return f'https://youtu.be/{best_video_id}'
