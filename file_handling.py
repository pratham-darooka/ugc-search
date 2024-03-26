import json
import os
from logger import logger
import re

def normalize_title(title):
    """Normalize title to snake_case."""
    title = title.lower()
    title = re.sub(r'\s+', '_', title)  # Replace spaces with underscores
    title = re.sub(r'[^\w\s]', '', title)  # Remove punctuation
    return title

def reset_directory(directory: str) -> None:
    os.makedirs(directory, exist_ok=True)  # Create the directory if it doesn't exist
    # Delete existing files in the directory
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        os.remove(file_path)

def save_post_to_file(url: str, post_title: str, post_content: str, post_comments: list[str], directory: str) -> None:
    os.makedirs(directory, exist_ok=True)  # Create the directory if it doesn't exist
    post_data = {
        "url": url,
        "post_title": post_title,
        "post_content": post_content,
        "post_comments": post_comments
    }

    post_id = url.split('/')[-3]

    file_path = os.path.join(directory, f'post_{post_id}_{post_title}.json')
    with open(file_path, 'w') as f:
        json.dump(post_data, f)

    logger.debug(f'Saved post to: post_{post_id}_{post_title}.json')

def save_transcript_to_file(video_data, directory) -> None:
    file_path = os.path.join(directory, f'transcript_{normalize_title(video_data['title'])}.json')

    # Convert dictionary to JSON string
    json_data = json.dumps(video_data, indent=4)

    # Save the transcript to a file
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(json_data)

    logger.debug(f'Saved transcript to: transcript_{normalize_title(video_data['title'])}.json')
