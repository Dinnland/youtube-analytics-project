from src.channel import Channel
from googleapiclient.errors import HttpError


class Video:
    """
    _класс для видео Video_
    id видео - video_id
    название видео - title
    ссылка на видео - url
    количество просмотров - viev_count
    количество лайков - like_count
    """
    def __init__(self, video_id: str) -> None:
        try:
            self.video_id = video_id
            self.youtube = Channel.get_service().videos().list(
                part='snippet,statistics,contentDetails,topicDetails', id=self.video_id
            ).execute()
            self.title = self.youtube["items"][0]["snippet"]["title"]
            self.url = 'https://www.youtube.com/watch?v=' + self.youtube['items'][0]['id']
            self.view_count = self.youtube['items'][0]['statistics']['viewCount']
            self.like_count = self.youtube['items'][0]['statistics']['likeCount']
        except IndexError:
            self.youtube = None
            self.title = None
            self.url = None
            self.viev_count = None
            self.like_count = None

    def __str__(self):
        return f'{self.title}'

    def __repr__(self):
        return f"{self.__class__.__name__}" \
               f"('{self.video_id}', {self.title}, {self.url}, {self.view_count}, {self.like_count})"


class PLVideo(Video):
    """класс для видео PLVideo(Video)"""

    def __init__(self, video_id, id_playlist):
        self.id = video_id
        self.id_playlist = id_playlist
        super().__init__(video_id)
