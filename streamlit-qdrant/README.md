# Intro
Hybrid similarity search can be a great way to construct a dataset for model
training. It can enable you to very efficiently label your dataset, and
potentially provides a framework which combines the benefits of deep learning
and traditional heuristics.

# Features

## Core

- [ ] Be able to run arbitrary similarity queries against the QDrant DB
- [ ] Summarize results
- [ ] Display images of the results
- [ ] Save the queries to sqlite

## Stretch

- [ ] Docker image
- [ ] Docker-compose with the streamlit app and qdrant set-up
- [ ] publish to PyPi
- [ ] Potential to concatenate embeddings for representation from ensemble

# Caveats

* I don't think the limits of what similarity and disimilarity can achieve
are well understood, nor how these dynamics relate to model and problem types
(e.g. object detection vs segmentation vs. classification vs.
multi-label classification etc.).

# Other comments to mention to Brian

- Requested that QDrant add in their swagger UI as part of their default deployment.
