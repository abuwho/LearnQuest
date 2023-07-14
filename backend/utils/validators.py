import re
from pytube import YouTube


class LinkValidator:
    def verify_link(self) -> bool:
        raise NotImplementedError
    
    def get_duration(self) -> int:
        raise NotImplementedError

class YoutubeValidator(LinkValidator):
    """
    Validator for YouTube links.

    Fields:
        link (str): The YouTube link to validate.

    """
    def __init__(self, link:str):
        self.link = link
        
    def verify_link(self) -> bool:
        """
        Verify if the link is a valid YouTube link.

        Returns:
            bool: True if the link is a valid YouTube link, else False.
        
        """
        regex_pattern = r'(?:https?:\/\/)?(?:www\.)?(?:youtube\.com|youtu\.be)\/(?:watch\?v=|embed\/|v\/)?([a-zA-Z0-9\-_]+)'
        match = re.match(regex_pattern, self.link)
        return match is not None
        
    
    # get duration of YouTube video using pytube
    def get_duration(self) -> int:
        """
        Get the duration of the YouTube video.

        Returns:
            int: The duration of the YouTube video in seconds. 
        
        """
        try:
            video = YouTube(self.link)
            duration = video.length
            return duration
        except Exception as e:
            print(f"Error occurred: {str(e)}\nReturning duration = 0")
            return 0

        
