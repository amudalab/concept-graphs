# Document retrieval over concept graphs

Builds concept graphs (adjacency matrices, taxonomies, enhanced semantic nets)
from document keyphrases and runs retrieval / graph-analysis algorithms over
them. Includes small `web.py` demos that serve the `static/` UI.

Run from this directory.

## Layout

```
document_retrieval/
├── graph_init.py          # was test.py — entry point that builds graphs
├── adjmatrix.py / edge.py / textmodel.py / textgraph.py
├── doc_ret_*.py           # retrieval variants (bag-of-words, BFS, edge/node enh.)
├── bfs*.py / taxonomy*.py / edge_enhancement*.py / …
├── ret_*.py               # web.py front-ends
├── static/                # CSS / JS for the web demos (must stay here)
├── archive/               # older alternate implementations
└── data/
    ├── corpus/                  # source documents
    ├── keys/                    # per-document keyphrase lists
    ├── wikipedia_articles/      # supporting Wikipedia text dumps
    ├── db/                      # master hierarchy graphs (.gdf)
    ├── doc_graphs/              # per-document graphs
    ├── taxonomies/              # per-document taxonomy graphs
    ├── enhanced_semantic_nets/  # edge-enhanced nets
    ├── doc_details/             # cluster / degree spreadsheets
    └── *.gdf / *.xls / …        # aggregated graph artefacts & query files
```

## Examples

```bash
python graph_init.py
python doc_ret_bag_of_words.py
python doc_ret_edge_enh.py
python bfs.py
python edge_enhancement.py
```

Python modules import each other by bare name (`from adjmatrix import …`,
`import graph_init`), so keep the working directory here (or put this folder on
`PYTHONPATH`).

## Note on `graph_init`

Previously named `test.py`, which conflicted with Python’s standard library
`test` package. All callers now `import graph_init`.
