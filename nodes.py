from tools import web_search
from state import Thumbnail
from prompts import PROMPT_WRITER_SYSTEM, PROMPT_WRITER_USER, REVISION_HINT, CRITIC_SYSTEM
from pydantic import BaseModel, Field
from dotenv import load_dotenv
load_dotenv()
from pathlib import Path
from openai import OpenAI
import base64
import re
import requests

outputs = Path(__file__).parent / "outputs"
outputs.mkdir(exist_ok=True)


def get_openai_client() -> OpenAI:
    return OpenAI()


class Critique(BaseModel):
    rating: int = Field(ge=1, le=10)
    feedback: str


# Node1
def node_search(state: Thumbnail) -> dict:
    summary = web_search(f"Youtube thumbnail ideas for: {state['topic']}")
    return {
        "search_summary": summary,
    }

#node2
def node_prompt_writer(state: Thumbnail) -> dict:
    feedback = ""
    if state.get("critique"):
        feedback = REVISION_HINT.format(rating=state["rating"], critique=state["critique"])
    user = PROMPT_WRITER_USER.format(
        topic=state['topic'],
        search_summary=state["search_summary"],
        feedback=feedback,
    )
    client = get_openai_client()
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": PROMPT_WRITER_SYSTEM},
            {"role": "user", "content": user},
        ],
    )
    current_prompt = response.choices[0].message.content.strip()
    return {
        "current_prompt": current_prompt,
    }

#node3
def node_generator(state: Thumbnail) -> dict:
    client = get_openai_client()
    n = state.get("iteration", 0) + 1
    resp = client.images.generate(
        model="gpt-image-2",
        prompt=state["current_prompt"],
        size="1920x1088",
        n=1,
    )

    print(f"DEBUG: Response type: {type(resp)}")
    
    path = Path(state["run_dir"]) / f"iter_{n}.png"
    if hasattr(resp.data[0], 'b64_json') and resp.data[0].b64_json:
        img_data = base64.b64decode(resp.data[0].b64_json)
        path.write_bytes(img_data)
    elif hasattr(resp.data[0], 'url') and resp.data[0].url:
        img_response = requests.get(resp.data[0].url)
        img_response.raise_for_status()
        path.write_bytes(img_response.content)
    else:
        raise ValueError(f"Image has neither URL nor b64_json.")

    return {
        "image_path": str(path),
        "iteration": n,
    }

#node4
def critic_node(state: Thumbnail) -> dict:
    prompt_text = (
        f"Topic: {state['topic']}\n"
        f"Prompt: {state['current_prompt']}\n"
        f"Please rate the generated thumbnail on a scale from 1 to 10 and provide constructive feedback. "
        f"The image is saved at {state['image_path']}."
    )
    client = get_openai_client()
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": CRITIC_SYSTEM},
            {"role": "user", "content": prompt_text},
        ],
    )
    text = response.choices[0].message.content.strip()
    match = re.search(r"(\d+)", text)
    rating = int(match.group(1)) if match else 0
    rating = max(1, min(rating, 10))

    history = state.get("history", []) + [{
        "iteration": state["iteration"],
        "prompt": state["current_prompt"],
        "image_path": state["image_path"],
        "rating": rating,
        "critique": text,
    }]

    return {
        "rating": rating,
        "critique": text,
        "history": history,
    }

#node5
def node_saver(state: Thumbnail) -> dict:
    history = state.get("history", [])
    lines = [
        f"# Thumbnail Run Results for: {state['topic']}",
        "",
        f"Target rating: {state['target_rating']}",
        f"Max iterations: {state['max_iterations']}",
        "",
    ]
    for entry in history:
        lines.extend([
            f"## Iteration {entry['iteration']}",
            f"- Prompt: {entry['prompt']}",
            f"- Rating: {entry['rating']}",
            f"- Critique: {entry['critique']}",
            f"- Image: ![Iteration {entry['iteration']}]({Path(entry['image_path']).name})",
            "",
        ])
    save_path = outputs / "save.md"
    save_path.write_text("\n".join(lines), encoding="utf-8")
    return {
        "save_path": str(save_path),
    }


Targetrating = 9
maxiteration = 3


#conditional 
def should_continue(state: Thumbnail):
    if state.get("rating", 0) >= Targetrating:
        return "saver"
    if state.get("iteration", 0) >= maxiteration:
        return "saver"
    return "prompt_writer"
