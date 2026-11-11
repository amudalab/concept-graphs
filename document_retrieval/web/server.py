"""Minimal web.py search server shared by the ``ret_*.py`` front-ends (internal)."""

from __future__ import annotations

import json
from typing import Callable

import web


def create_app(search: Callable[[str], list[str]]) -> web.application:
    """Create a web.py app serving ``/search/<query>`` and redirecting the rest to ``/static/``."""

    class SearchHandler:
        def GET(self, query: str) -> str:
            return json.dumps(search(query))

    class StaticHandler:
        def GET(self, name: str) -> None:
            raise web.seeother("/static/" + name)

    urls = (
        "/search/(.*)", "SearchHandler",
        "/(.*)", "StaticHandler",
    )
    return web.application(
        urls, {"SearchHandler": SearchHandler, "StaticHandler": StaticHandler}
    )


def run_server(search: Callable[[str], list[str]]) -> None:
    """Serve ``search`` over HTTP (port taken from ``sys.argv`` as in web.py)."""
    create_app(search).run()
