# Concept explorer

A [Processing](https://processing.org/) (Java mode) sketch for browsing concept
subgraphs and linked PDF resources.

## Open in Processing

1. Install Processing and select **Java** mode.
2. Open the `concept_explorer` folder (the main file must be named
   `concept_explorer.pde` to match the folder — Processing’s convention).
3. Run the sketch.

## Layout

```
concept_explorer/
├── concept_explorer.pde   # main sketch
├── pdf_reader.pde         # desktop PDF opener helper
├── subgraph.py            # offline subgraph extraction utility
├── sketch.properties
├── AndroidManifest.xml    # legacy Android export metadata
└── data/                  # images, JSON indices, sample .gdf graphs
```

`loadImage` / `loadJSONArray` resolve files from `data/` automatically.
`subgraph.py` expects to be run from this folder so `data/dsfull1.gdf` resolves.
