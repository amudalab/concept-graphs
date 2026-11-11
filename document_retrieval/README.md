# Document retrieval over concept graphs

Builds concept graphs from document keyphrases and runs retrieval /
graph-analysis algorithms over them.

Requires **Python 3.10+**. Run every command from this directory.

## Layout

```
document_retrieval/
├── core/         # edge, adjacency, text_model, text_graph, graph_init, gdf_io
├── retrieval/    # bag_of_words, edge_enhanced, node_degree, node_term_freq, …
├── analysis/     # bfs, betweenness, closeness, degree, prim, shortest paths, …
├── taxonomy/     # taxonomy builders, edge enhancement, EM clustering
├── web/          # web.py front-ends + static/
├── tools/        # extract_phrases, extract_keys, text_convert
├── archive/      # legacy Python 2 snapshots (not maintained)
└── data/         # corpora, keys, graphs
```

## Examples

```bash
python -m core.graph_init
python -m retrieval.bag_of_words "stack queue tree"
python -m retrieval.node_degree "binary search tree"
python -m analysis.bfs
python -m web.bag_of_words
```
