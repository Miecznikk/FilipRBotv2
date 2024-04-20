import os
import random
import re
import threading
from queue import Queue

import pytube.exceptions
from moviepy.audio.io.AudioFileClip import AudioFileClip
from pytube import YouTube, Playlist
from pytube.exceptions import VideoUnavailable, RegexMatchError

SAVE_PATH = 'media/youtube/'
PLAYLIST_URL = 'https://www.youtube.com/playlist?list=PLoCdz18259OfZIQr3SVp9eFiIHaIz62C7'


class VideoTooLong(Exception):
    def __init__(self, message="Video too long"):
        self.message = message
        super().__init__(self.message)


class YoutubeMusicController:
    @classmethod
    def download_single_song(cls, video_url, tmp=""):
        try:
            yt = YouTube(video_url)
            if yt.length > 10 * 60:
                raise VideoTooLong(f"Video {video_url} too long: {yt.length}")
            else:
                safe_title = cls.get_song_safe_title(yt.title)
                existing_tmp_songs = cls.get_tmp_existing_songs_titles()
                if f"{safe_title}.mp3" in existing_tmp_songs:
                    return f"{tmp}{SAVE_PATH}{safe_title}.mp3"
                existing_songs = cls.get_existing_songs_titles()
                if f"{safe_title}.mp3" in existing_songs:
                    return f"{SAVE_PATH}{safe_title}.mp3"
                audio_stream = yt.streams.filter(only_audio=True).first()
                audio_stream.download(output_path=tmp + SAVE_PATH, filename=f'{safe_title}.mp4')
                audio_clip = AudioFileClip(tmp + SAVE_PATH + f'{safe_title}.mp4')
                audio_clip.write_audiofile(tmp + SAVE_PATH + f'{safe_title}.mp3')

                audio_clip.close()
                os.remove(tmp + SAVE_PATH + f'{safe_title}.mp4')
                return tmp + SAVE_PATH + f'{safe_title}.mp3'
        except VideoUnavailable as e:
            raise e
        except RegexMatchError as e:
            raise e

    @classmethod
    def get_all_songs_randomly_shuffled(cls):
        all_songs = os.listdir(SAVE_PATH)
        random.shuffle(all_songs)
        return [SAVE_PATH + song for song in all_songs]

    @staticmethod
    def delete_all_songs_from_save_path():
        for file in os.listdir(SAVE_PATH):
            os.remove(os.path.join(SAVE_PATH, file))

    @staticmethod
    def get_existing_songs_titles():
        return os.listdir(SAVE_PATH)

    @staticmethod
    def get_tmp_existing_songs_titles():
        return os.listdir("tmp/" + SAVE_PATH)

    @staticmethod
    def get_song_safe_title(title):
        return re.sub(r'[\\/:"*?<>|]+', '-', title)

    @staticmethod
    def get_all_videos_urls_in_playlist(playlist_url):
        playlist = Playlist(playlist_url)
        return playlist.video_urls

    @staticmethod
    def delete_all_tmp_songs():
        tmp_files = os.listdir("tmp/" + SAVE_PATH)
        for file in tmp_files:
            os.remove(os.path.join("tmp/" + SAVE_PATH, file))

    @classmethod
    def download_all_songs_from_playlist(cls):
        video_urls = cls.get_all_videos_urls_in_playlist(PLAYLIST_URL)
        queue = Queue()
        num_threads = min(8, len(video_urls))
        threads = []

        for _ in range(num_threads):
            t = threading.Thread(target=worker, args=[queue])
            t.start()
            threads.append(t)

        for video_url in video_urls:
            queue.put(video_url)

        for _ in range(num_threads):
            queue.put(None)

        for t in threads:
            t.join()


def worker(queue):
    while True:
        video_url = queue.get()
        if video_url is None:
            break
        try:
            YoutubeMusicController.download_single_song(video_url)
        except pytube.exceptions.AgeRestrictedError:
            print('AgeRestrictedError')
        queue.task_done()
