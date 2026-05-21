from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
import os
from pathlib import Path
from datetime import datetime

from graph import build_graph

app = FastAPI()

BASE_DIR = Path(__file__).resolve().parent

# Mount the static and outputs directories
app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")
app.mount("/outputs", StaticFiles(directory=str(BASE_DIR / "outputs")), name="outputs")

class GenerateRequest(BaseModel):
    topic: str

@app.post("/api/generate")
async def generate_thumbnail(req: GenerateRequest):
    if not req.topic:
        raise HTTPException(status_code=400, detail="Topic is required")
        
    run_dir = Path(__file__).parent / "outputs" / datetime.now().strftime("%Y%m%d_%H%M%S")
    run_dir.mkdir(parents=True, exist_ok=True)

    graph = build_graph()
    initial = {
        "topic": req.topic,
        "target_rating": 8,
        "max_iterations": 3,
        "iteration": 0,
        "rating": 0,
        "critique": "",
        "history": [],
        "run_dir": str(run_dir),
    }
    
    try:
        final = graph.invoke(initial)
        
        # Calculate relative path to image from the outputs folder
        image_path = Path(final.get("image_path", ""))
        rel_path = f"{image_path.parent.name}/{image_path.name}"
        
        return {
            "success": True,
            "final_rating": final.get("rating", 0),
            "final_iteration": final.get("iteration", 0),
            "image_url": f"/outputs/{rel_path}",
            "critique": final.get("critique", ""),
            "prompt": final.get("current_prompt", "")
        }
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
async def read_index():
    return FileResponse(str(BASE_DIR / "static" / "index.html"))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
