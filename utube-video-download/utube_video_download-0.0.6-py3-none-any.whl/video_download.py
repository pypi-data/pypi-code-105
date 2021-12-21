import os
import re
import requests
import functools
from requests.models import Response
from tqdm import tqdm
from pytube import YouTube, Playlist

from youtube import console


def arrange_video_title(func):

    @functools.wraps(func)
    def wrapper(*args):

        yt_url, folder_path, title = args # unpacks the arguments of the download func

        # removes special characters from the video title
        mod_title: str = re.sub(r'[|!@#$%^&*()+-\/,]', '', title)

        return func(yt_url, folder_path, mod_title)
    
    return wrapper

@arrange_video_title        
def download(yt_url: str, folder_path: str, title: str) -> str or None:

    chunk_size: int = 1024

    r: Response = requests.get(yt_url, stream=True)

    total_file_size: int = int(r.headers['content-length'])

    file_path: str = os.path.join(folder_path, f'{title}.mp4')

    with open(f'{file_path}', 'wb') as f:

        if len(title) > 25:
            print(f'Downloading {title[:35]}...')
        else:
            print(f'Downloading {title}')
        
        try:
            for data in tqdm(iterable=r.iter_content(chunk_size=chunk_size),
                            leave=True,
                            total=total_file_size / chunk_size,
                            unit='KB',
                            dynamic_ncols=True,
                            colour='green',
                            ):
                f.write(data)
        except requests.exceptions.ChunkedEncodingError as e:
            print(e)
            return 
        else:
            console.print(':white_check_mark: ', end='')
            console.print(f'[green]{title} successfully downloaded[/]') 

    return "Done"

            
def single_video(url: str, folder_path: str) -> None:
    """Single video downloader function

    Args:
        url (str): The url of the youtube video to download
        folder_path (str): The path to which the folder should be saved
    """
    yt = YouTube(url)

    stream = yt.streams.filter(
        file_extension='mp4',
        progressive=True).get_by_itag(22)

    yt_url: str = stream.url

    title: str = stream.title

    return download(yt_url, folder_path, title)

def playlist_video(url: str, folder_path: str) -> None:
    """ Playlist downloader function

    Args:
        url (str): The url of the playlist video to download
        folder_path (str): The path to which the folder should be saved
    """

    playlist = Playlist(url)

    playlist_folder = os.path.join(folder_path, playlist.title)

    try:
        os.mkdir(playlist_folder)
    except Exception as e:
        print(e)
    finally:
        for yt_url in playlist.video_urls:
            single_video(yt_url, folder_path=playlist_folder)


if __name__ == '__main__':
    pass
