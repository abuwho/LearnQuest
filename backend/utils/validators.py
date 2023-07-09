import youtube_dl
import re


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
        
    
    def get_duration(self) -> int:
        ydl_opts = {'quiet': True}
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(self.link, download=False)
            duration = info.get('duration')
            return duration
    
