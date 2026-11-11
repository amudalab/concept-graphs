"""web.py front-end serving bag-of-words document retrieval."""

from __future__ import annotations

from web.server import run_server
from retrieval.bag_of_words import retrieve_documents

if __name__ == "__main__":
    run_server(retrieve_documents)
