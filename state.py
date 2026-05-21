from typing import TypedDict

class Thumbnail(TypedDict, total=False):
    topic: str
    rating: int
    iteration: int
    search_summary: str
    current_prompt: str
    image_path: str
    critique: str
    history: list
    target_rating: int
    max_iterations: int
    run_dir: str
    save_path: str






