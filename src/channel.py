import json
import os
from googleapiclient.discovery import build


class Channel:
    """Класс для ютуб-канала"""
    api_key: str = os.getenv('YT_API_KEY')
    youtube = build('youtube', 'v3', developerKey=api_key)

    def __init__(self, channel_id: str) -> None:
        """
        Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API.
        - id канала
        - название канала
        - описание канала
        - ссылка на канал
        - количество подписчиков
        - количество видео
        - общее количество просмотров
        """
        self.__channel_id = channel_id

        channel_info = self.youtube.channels().list(id=channel_id, part='snippet,statistics').execute()

        self.title = channel_info["items"][0]["snippet"]["title"]
        self.description = channel_info["items"][0]["snippet"]['description']
        self.url = f"https://www.youtube.com/channel/{channel_info['items'][0]['id']}"
        self.subscriber_count = channel_info["items"][0]['statistics']['subscriberCount']
        self.video_count = channel_info["items"][0]['statistics']['videoCount']
        self.view_count = channel_info["items"][0]['statistics']['viewCount']

    def __str__(self):
        return f"'{self.title} ({self.url})'"

    def __add__(self, other):
        """Складывает два канала между собой по количеству подписчиков."""
        return int(self.subscriber_count) + int(other.subscriber_count)

    def __sub__(self, other):
        """Вычитает два канала между собой по количеству подписчиков."""
        return int(self.subscriber_count) - int(other.subscriber_count)

    def __le__(self, other):
        """ метод для операции сравнения «меньше или равно»"""
        return int(self.subscriber_count) <= int(other.subscriber_count)

    def __lt__(self, other):
        """метод для операции сравнения «меньше»"""
        return int(self.subscriber_count) < int(other.subscriber_count)

    def __gt__(self, other):
        """метод для операции сравнения «больше»"""
        return int(self.subscriber_count) > int(other.subscriber_count)

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        channel = self.youtube.channels().list(id=self.channel_id, part='snippet,statistics').execute()
        print(json.dumps(channel, indent=2, ensure_ascii=False))

    @classmethod
    def get_service(cls):
        """
        возвращаtn объект для работы с YouTube API
        """
        return cls.youtube

    @property
    def channel_id(self):
        return self.__channel_id

    def to_json(self, path):
        """
        метод, сохраняющий в файл значения атрибутов экземпляра `Channel`
        """
        with open(path, 'w', encoding='utf-8') as file:
            json.dump(self.__dict__, file, ensure_ascii=False)
