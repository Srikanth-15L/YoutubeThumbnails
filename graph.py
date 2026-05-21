from langgraph.graph import StateGraph, END, START

from state import Thumbnail
from nodes import (
    node_generator, node_prompt_writer,
    node_search, critic_node, should_continue, node_saver
)


def build_graph():
    graph = StateGraph(Thumbnail)
    graph.add_node("websearch", node_search)
    graph.add_node("prompt_writer", node_prompt_writer)
    graph.add_node("generator", node_generator)
    graph.add_node("critic", critic_node)
    graph.add_node("saver", node_saver)

    graph.add_edge(START, "websearch")
    graph.add_edge("websearch", "prompt_writer")
    graph.add_edge("prompt_writer", "generator")
    graph.add_edge("generator", "critic")
    graph.add_conditional_edges("critic", should_continue,
                               {
                                   "prompt_writer": "prompt_writer",
                                   "saver": "saver"
                               })

    return graph.compile()