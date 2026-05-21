from pathlib import Path
from datetime import datetime

from youtube_thumbnailer.graph import build_graph






def main():
    topic = "why python is best language"
    run_dir = Path(__file__).parent / "outputs" / datetime.now().strftime("%Y%m%d_%H%M%S")
    run_dir.mkdir(parents=True, exist_ok=True)

    graph = build_graph()
    initial = {
        "topic": topic,
        "target_rating": 8,
        "max_iterations": 3,
        "iteration": 0,
        "rating": 0,
        "critique": "",
        "history": [],
        "run_dir": str(run_dir),
    }
    final = graph.invoke(initial)
    print(f"\nfinalrating:{final.get('rating', 0)}/10 after final_iteration:{final.get('iteration', 0)}")
    print(f"Results saved to: {final.get('save_path')}")


if __name__ == "__main__":
    main()
