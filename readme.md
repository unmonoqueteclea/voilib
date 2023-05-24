# voilib: podcast search engine

# final check
- time in logs
- add episodes from twitter user
## files
├── backend
│   ├── readme.md
│   └── src
│       ├── voilib
│       │   ├── cli
│       │   │   ├── checks.py
│       │   │   ├── episodes.py
│       │   ├── __init__.py
│       │   ├── routers
│       │   │   ├── media.py
│       │   ├── tasks.py
│       │   ├── tests
│       │   │   ├── conftest.py
│       │   │   ├── __init__.py
│       │   │   ├── test_analytics.py
│       │   │   ├── test_app.py
│       │   │   ├── test_collection.py
│       │   │   ├── test_media.py
│       │   │   ├── test_storage.py
│       │   │   ├── test_transcription.py
│       │   │   ├── test_users.py
│       │   │   └── test_vector.py
│       │   ├── transcription.py
│       │   ├── vector.py
│       │   └── worker.py
├── frontend
│   ├── index.html
│   ├── jsconfig.json
│   ├── makefile
│   ├── nginx.conf
│   ├── package.json
│   ├── package-lock.json
│   ├── README.md
│   ├── src
│   │   ├── api.js
│   │   ├── App.svelte
│   │   ├── assets
│   │   │   └── svelte.svg
│   │   ├── lib
│   │   │   ├── app.js
│   │   │   ├── CardQueryResult.svelte
│   │   │   ├── DemoQueries.svelte
│   │   │   ├── Hero.svelte
│   │   │   ├── PageFooter.svelte
│   │   │   ├── PageHeader.svelte
│   │   │   ├── pages
│   │   │   │   ├── About.svelte
│   │   │   │   ├── Content.svelte
│   │   │   │   ├── Home.svelte
│   │   │   │   └── Query.svelte
│   │   │   ├── Player.svelte
│   │   │   ├── StretchSpinner.svelte
│   │   │   └── WaveSpinner.svelte
│   │   ├── routes.js
├── infra
│   ├── development
│   │   ├── compose.yml
│   │   └── traefik.dev.toml
│   ├── makefile
│   ├── production
│   │   ├── cert
│   │   ├── compose.yml
│   │   └── traefik.prod.toml
│   └── readme.md
└── readme.md


# cron
crontab -e

```
# update list of episodes every 6 hours
0 */6 * * * cd /home/accushoot/voilib/infra/development && docker compose --env-file=.env.dev exec worker voilib-episodes --update

# transcribe last day episodes every 12 hours
20 */12 * * * cd /home/accushoot/voilib/infra/development && docker compose --env-file=.env.dev exec worker voilib-episodes --transcribe-days 1

# calculate pending embeddings every 6 hours
40 */6 * * * cd /home/accushoot/voilib/infra/development && docker compose --env-file=.env.dev exec worker voilib-episodes --store


```





# quickstart
To run all the services locally, just do (from [./voilib-infra](./voilib-infra)):

```console
docker compose up --build
```

After everything is built, the following urls will be available:

- `pgadmin`: Will be running at `localhost:5050`
- `swagger` API docs running at `api.localhost/docs`
- `redoc` API docs running at `api.localhost/redoc`
- `traefik` dashboard at `localhost:8080`


BERT (and other transformer networks) output an embedding for each
token in our input text. In order to create a fixed-sized sentence
embedding out of this, sentence transformers apply mean pooling, i.e.,
the output embeddings for all tokens are averaged to yield a
fixed-sized vector. The sentences (texts) are mapped such that
sentences with similar meanings are close in vector space. One common
method to measure the similarity in vector space is to use cosine
similarity.

See https://www.sbert.net/examples/applications/semantic-search/README.html#symmetric-vs-asymmetric-semantic-search  # noqa

For asymmetric semantic search, you usually have a short query (like a
question or some keywords) and you want to find a longer paragraph
answering the query.

See https://www.sbert.net/docs/pretrained_models.html

This module defines some contants such us:

- FRAGMENT_WORDS:
  See https://www.sbert.net/examples/applications/computing-embeddings/README.html#input-sequence-length  # noqa

  Transformer models like BERT / RoBERTa / DistilBERT etc. the runtime
  and the memory requirement grows quadratic with the input
  length. This limits transformers to inputs of certain lengths. A
  common value for BERT & Co. are 512 word pieces, which correspond to
  about 300-400 words (for English). Longer texts than this are
  truncated to the first x word pieces.

  By default, the provided methods use a limit fo 128 word pieces,
  longer inputs will be truncated. Average sentence length is 15-20
  words

- DEFAULT_TRANSFORMER_MODEL:

  Default model produces normalized embedding and can be used with
  dot-product, cosine-similarity or euclidean distance (all three
  scoring function will produce the same results).

- EMBEDDINGS_SIZE: Size of the generated embedding vectors
