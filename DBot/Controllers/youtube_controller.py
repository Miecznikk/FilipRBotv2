import os
import re
import threading
from queue import Queue

import pytube.exceptions
from moviepy.audio.io.AudioFileClip import AudioFileClip
from pytube import YouTube, Playlist

SAVE_PATH = 'media/youtube/'
PLAYLIST_URL = 'https://www.youtube.com/playlist?list=PLoCdz18259OfZIQr3SVp9eFiIHaIz62C7'


def delete_all_songs_from_save_path():
    for file in os.listdir(SAVE_PATH):
        os.remove(os.path.join(SAVE_PATH, file))


def get_all_videos_urls_in_playlist(playlist_url):
    playlist = Playlist(playlist_url)
    return playlist.video_urls


def get_existing_songs_titles():
    return os.listdir(SAVE_PATH)


def safe_filename(title):
    return re.sub(r'[\\/:"*?<>|]+', '-', title)


def worker(queue):
    while True:
        video_url = queue.get()
        if video_url is None:
            break
        try:
            download_single_video_mp3(video_url)
        except pytube.exceptions.AgeRestrictedError:
            print('AgeRestrictedError')
        queue.task_done()


def download_single_video_mp3(video_url):
    existing_songs = get_existing_songs_titles()
    yt = YouTube(video_url)
    if yt.length < 10 * 60:
        safe_title = safe_filename(yt.title)
        if safe_title + ".mp3" in existing_songs:
            return 'media/youtube/' + safe_title + ".mp3"
        audio_stream = yt.streams.filter(only_audio=True).first()
        audio_stream.download(output_path="tmp/" + SAVE_PATH, filename=f'{safe_title}.mp4')

        audio_clip = AudioFileClip("tmp/" + SAVE_PATH + f'{safe_title}.mp4')
        audio_clip.write_audiofile("tmp/" + SAVE_PATH + f'{safe_title}.mp3')

        audio_clip.close()
        os.remove("tmp/" + SAVE_PATH + f'{safe_title}.mp4')
        return "tmp/" + SAVE_PATH + f'{safe_title}.mp3'


def main():
    global SAVE_PATH
    SAVE_PATH = "../media/youtube/"
    video_urls = get_all_videos_urls_in_playlist(PLAYLIST_URL)
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


if __name__ == "__main__":
    main()
