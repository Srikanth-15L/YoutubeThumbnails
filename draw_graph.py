from graph import build_graph

try:
    graph = build_graph()
    print("Generating graph image...")
    graph.get_graph().draw_mermaid_png(output_file_path="graph.png")
    print("Successfully saved graph.png")
except Exception as e:
    print(f"Could not draw mermaid graph: {e}")
