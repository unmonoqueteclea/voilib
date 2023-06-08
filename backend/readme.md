# Voilib - backend documentation
Backend and API of **Voilib**, written in Python using
[FastAPI](https://fastapi.tiangolo.com/).

![CI](https://github.com/unmonoqueteclea/voilib/actions/workflows/backend.yml/badge.svg)

For development, install the project locally with `pip install -e
.[dev]` to ensure you use editable mode. Development dependencies such
as `ruff`, `black` or `pytest` will be also installed when you use
that command.

ℹ️ You should read very carefully the main [readme](../readme.md) and
the [deployment docs](../infra/readme.md). You will find there
instructions to run all the app services using Docker and the needed
commands to start populating the application with content.

## REST API
Voilib offers a **REST API** with some public endpoints and some
admin-only endpoints using `JWT`-based authentication. All the
endpoints are documented and exposed through `Swagger` at
[0.0.0.0:8080/docs](http://0.0.0.0:8080/docs) if running the project
locally or
[http://localhost/service/docs](http://localhost/service/docs) when
running the project using the provided `Docker Compose` configuration
(`Traefik` is serving the API).

Voilib frontend consumes this **REST API** (currently, just the
unauthenticated endpoints)

## settings
All the application settings are defined in
[settings.py](./src/voilib/settings.py) module.  That module contains
default values for all the settings (those default values are used
when running the application locally, without Docker). In Docker-based
deployments, those settings will be usually taken automatically from
environment variables.

You can use settings in any app module like this:

```python
from voilib.settings import settings

print(settings.redis_host)
```

## scripts
The Voilib Python package includes some scripts to do some common
tasks such as **updating episodes** from the list of feeds or
**transcribing episodes** from the last X days. All the available
tasks are defined in `[options.entry_points]` in
[setup.cfg](./setup.cfg) file. You can use `--help` to see all their
options, e.g. `voilib-checks --help` or `voilib-episodes --help`.

In the [first-run-tasks section of deployment
docs](../infra/readme.md#first-run-tasks) we are using those scripts
to add new collect podcast episodes, transcribe them or index pending
episodes that are already transcribed. We just use `cron` to automate
them but you can use any other technology you want that is able to
trigger Python scripts.

## databases
Voilib uses two databases:

- A **relational `SQLite` database** stores some metadata about podcasts
  and their episodes. See [db.py](./src/voilib/db.py)
- A **vector database**, [Qdrant](https://qdrant.tech/), stores
  embeddings of episodes transcription fragments. By default, in tests
  and local development that database is just a file stored locally
  without the need of any other service. In production, we are
  lunching a `Qdrant` container. See
  [vector.py](./src/voilib/vector.py). Connection data is defined in
  [settings.py](./src/voilib/settings.py)

## asynchronous tasks with rq
Some tasks such as **transcribing** or **calculating embeddings** are
very long and can't be done in the some process that is answering API
requests. That's why we used an extremely simple job queues system,
[rq](https://python-rq.org/), using [Redis](https://redis.io/) as its
message broker. It's configured in [worker.py
module](./src/voilib/worker.py).

Check [tasks.py module](./src/voilib.tasks.py) to see some examples of
functions adding new tasks to the queue that will be executed by the
worker service (in the provided infrastructure configuration, it will
run in a different container).


## episodes transcription
For transcription (see
[transcription.py](./src/voilib/transcription.py) module) Voilib uses
[Whisper: Open AI's Open Source Transcription
Model](https://openai.com/research/whisper), running locally with the
help of [whisper-jax](https://github.com/sanchit-gandhi/whisper-jax)
library.

The output of the transcription of an episode is a `CSV` file (using
character `|` as separator) with the following structure:

```
start_time | end_time | transcribed_sentence
```

All the transcriptions are stored in the `media folder` (defined in
[settings.py](./src/voilib/settings.py)).


## embeddings calculation
The calculation of embeddings is performed by the [Sentence
Transformers](https://www.sbert.net/) library, a Python framework for
state-of-the-art sentence, text and image embeddings.

**BERT** (and other transformer networks) output an embedding for each
token in our input text. In order to create a fixed-sized sentence
embedding out of this, sentence transformers apply *mean pooling*,
i.e., the output **embeddings for all tokens are averaged** to yield a
**fixed-sized vector**. The sentences (texts) are mapped such that
sentences with similar meanings are close in vector space. One common
method to measure the similarity in vector space is to use cosine
similarity.

For **asymmetric semantic search**, Voilib use case, you usually have a
short query (like a question or some keywords) and you want to find a
longer paragraph answering the query. See  https://www.sbert.net/examples/applications/semantic-search/README.html#symmetric-vs-asymmetric-semantic-search.

For transformer models like BERT / RoBERTa / DistilBERT etc. the
runtime and the memory requirement grows quadratic with the input
length. This limits transformers to inputs of certain lengths. A
common value for BERT & Co. are 512 word pieces, which correspond to
about 300-400 words (for English).

If models that produce normalized embeddings are used, those embeddings
can be used with dot-product, cosine-similarity or euclidean distance
(all three scoring function will produce the same results).

All the embedding calculation configuration and main functions can be
found in [embedding.py module](./src/voilib/embedding.py).


## contributing
ℹ️ You should read very carefully the main [readme](../readme.md) and
[deployment docs](./infra/readme.md). You will find there instructions
to run all the app services using Docker and the [first run
tasks](../infra/readme.md#first-run-tasks).

- If you just want to run the backend locally, without Docker, you can
do `make start`. After that, you will find `Swagger` in
[0.0.0.0:8080/docs](http://0.0.0.0:8080/docs). Then, if it is the
first time you run the project locally, run `make migrate` to ensure
all the needed tables are created in the `SQLite` database.

- The same [makefile](./makefile) contains other targets for common
tasks such as creating migrations or applying them. Run `make` to see
all the available targets.

- Check [scripts section](#scripts) to see how to run the main scripts
that will help you populating the app with your own content.

- You can also execute `pytest` to run all the **backend tests**.
