"""web.py front-end serving degree-based document retrieval."""

from __future__ import annotations

from web.server import run_server
from retrieval.node_degree import retrieve_documents

if __name__ == "__main__":
    run_server(retrieve_documents)
