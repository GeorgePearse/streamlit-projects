# Intro - Interactive Classifier Development
Hybrid similarity search can be a great way to construct a dataset for model
training. It can enable you to very efficiently label your dataset, and
potentially provides a framework which combines the benefits of deep learning
and traditional heuristics.

Allows you to quickly, and interactively, carve out a subclass.

Also excellent for constructing unit tests (small and specific datasets that the model performs poorly on that should be particular areas of focus).

Construct with a small dataset returned and then enlarge to see how well it has worked (much like using limit to check your query in SQL).

# Features

## Core

- [X] Be able to run arbitrary similarity queries against the QDrant DB
- [X] Summarize results
- [X] Display images of the results
- [ ] Save the queries to sqlite -> went with file instead, much easier to read
- [ ] Tidy the code
- [ ] Save some good example queries

## Messy things to fix

- [ ] Too much code duplication for things like getting the examples

## Stretch

- [ ] For it to generalise well to other teams you'd also need to display the positive and negative examples
- [ ] Save query results to disk (for now)
- [ ] Docker image
- [ ] Docker-compose with the streamlit app and qdrant set-up
- [ ] publish to PyPi
- [ ] Potential to concatenate embeddings for representation from ensemble
- [ ] Pagination of the response

## Potential Improvements

- [ ] Download any prior CSV via a separate page and remove the download option
from the post page
- [ ] Seperate query running from query saving (but then you wouldn't be able to neatly save the results of queries)

# Caveats

* I don't think the limits of what similarity and disimilarity can achieve are well understood, nor how these dynamics relate to model and problem types (e.g. object detection vs segmentation vs. classification vs.multi-label classification etc.).
* Not sure if you would actually wrap the API in a real solution.

# Choices

## Why DB storage over files?

### Pros
* Can easily search through the strings this way (e.g. all the queries that contain X).
* Much more scalable (in theory)

### Cons
* The problem with this is that json is always a nightmare to store in databases, even if encoded and then decoded as a string. Turned out that really wasn't worth it.

# Other comments to mention to Brian

- Requested that QDrant add in their swagger UI as part of their default deployment.

# Examples

- The surgical clips
- The black images
