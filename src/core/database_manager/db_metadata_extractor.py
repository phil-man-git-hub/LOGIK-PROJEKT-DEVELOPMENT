"""Stubs for media metadata extraction used by the monitor service.

These are minimal implementations to be extended in Phase 2 (ffmpeg/Pillow usage).
"""

from typing import Dict


def extract_asset_metadata(file_path: str, mime_type: str) -> Dict:
    """Return basic metadata dict for a file path and mime type.

    Currently a stub returning minimal structure. Phase 2 will fill this in with ffmpeg/Pillow.
    """
    metadata = {}

    if mime_type and mime_type.startswith('image/'):
        metadata.update({'asset_type': 'image'})
    elif mime_type and mime_type.startswith('video/'):
        metadata.update({'asset_type': 'video'})
    elif mime_type and mime_type.startswith('audio/'):
        metadata.update({'asset_type': 'audio'})
    else:
        metadata.update({'asset_type': 'other'})

    return metadata
