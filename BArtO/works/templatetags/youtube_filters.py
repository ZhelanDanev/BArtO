from django import template
from urllib.parse import urlparse, parse_qs

register = template.Library()

@register.filter
def youtube_embed(url):
    """
    Converts a standard YouTube URL into an embed-friendly URL.
    """
    parsed_url = urlparse(url)
    if parsed_url.hostname in ['www.youtube.com', 'youtube.com']:
        query_params = parse_qs(parsed_url.query)
        video_id = query_params.get('v')
        if video_id:
            return f"https://www.youtube.com/embed/{video_id[0]}"
    elif parsed_url.hostname == 'youtu.be':
        return f"https://www.youtube.com/embed{parsed_url.path}"
    return url  # Return the original URL if it's not a YouTube link.
