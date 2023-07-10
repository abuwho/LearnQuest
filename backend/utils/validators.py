import re
from pytube import YouTube


class LinkValidator:
    def verify_link(self) -> bool:
        raise NotImplementedError
    
    def get_duration(self) -> int:
        raise NotImplementedError

class YoutubeValidator(LinkValidator):
    def __init__(self, link:str):
        self.link = link
        
    def verify_link(self) -> bool:
        regex_pattern = r'(?:https?:\/\/)?(?:www\.)?(?:youtube\.com|youtu\.be)\/(?:watch\?v=|embed\/|v\/)?([a-zA-Z0-9\-_]+)'
        match = re.match(regex_pattern, self.link)
        return match is not None
        
    
    # get duration of YouTube video using pytube
    def get_duration(self) -> int: 
        try:
            video = YouTube(self.link)
            duration = video.length
            return duration
        except Exception as e:
            print(f"Error occurred: {str(e)}\nReturning duration = 0")
            return 0

        
