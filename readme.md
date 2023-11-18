# Voilib: Open Source Podcast Search Engine 🔍

Voilib offers **semantic search** in thousands of minutes of
high-quality transcriptions of podcasts. Just type your query and it
will find related content in thousands of episodes. Voilib also allows
users to index their own audio files.

![](https://github.com/unmonoqueteclea/voilib/actions/workflows/backend.yml/badge.svg)
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)

🎧 **Try it now** for free at [voilib.com](https://voilib.com/)!

> Voilib doesn't offer any paid service. Help me ensure the continued
> availability and accessibility of it by supporting me through
> donations. You will directly contribute to covering the server
> expenses and enable me to maintain and improve Voilib for users
> worldwide. [Customized
> assistance](https://ko-fi.com/unmonoqueteclea/commissions) is also
> offered.
>
> <a href='https://ko-fi.com/Z8Z7M4I8K'
> target='_blank'><img height='36' style='border:0px;height:36px;'
> src='https://storage.ko-fi.com/cdn/kofi3.png?v=3' border='0' alt='Buy
> Me a Coffee at ko-fi.com' /></a>

![Voilib](./docs/voilib.gif)

## ▶️ run your own instance now!

You can run **your own instance** of Voilib in your server, it
doesn't depend on any external paid service.

```
mkdir voilib && cd "voilib"
curl https://raw.githubusercontent.com/unmonoqueteclea/voilib/main/compose.yml -o compose.yml
docker compose up
```

> You will need an admin user and password. By default user
> `voilib-admin` with password `*audio*search*engine` will be
> created.

> You can change default ports with environment variables:
> - `VOILIB_MANAGEMENT_PORT` (for management page: default 8501)
> - `VOILIB_FRONTEND_PORT` (for frontend: default 80)
> - `VOILIB_API_PORT` (for backend: default 81)

After all services are up, jump to
[http://localhost:8501](http://localhost:8501) and follow the
instructions to populate Voilib with content. You can also check
[first run tasks section](./infra/readme.md#first-run-tasks).

![Management](./docs/management.png)

More information about deployments in
[infra/readme](./infra/readme.md).


## ❓ how it works
Voilib performs 4 main tasks: **collecting**, **transcribing**,
**indexing** and **querying** podcasts episodes to find the most
interesting fragments for every user prompt.

- **collection**: Almost all public podcasts have an associated `RSS
  feed` that contains **metadata** about every episode and a link to
  the **audio file**. Voilib uses those feeds to **collect and store**
  that metadata from the list of podcasts configured by the
  application admin. Additionally, Voilib can also index your own
  audio files.

- **transcription**: The collected episodes are then transcribed using
  [Whisper: Open AI's Open Source Transcription
  Model](https://openai.com/research/whisper).

- **index**: Episodes transcripts are divided into **fragments of
  approximately 40 words** (check `DEFAULT_FRAGMENT_WORDS` constant to
  see the value currently used). Then, Voilib calculates the
  [embedding](https://en.wikipedia.org/wiki/Sentence_embedding) of
  each fragment. In that way, every fragment is converted into a
  vector of 384 floating point numbers (check `EMBEDDINGS_SIZE`
  constant to see the embedding size currently used). Those vectors
  are stored in a [vector database: Qdrant](https://qdrant.tech/).

- **queries**: For each new user prompt, Voilib just needs to
  calculate the embedding of it and find the closest ones in the
  vector database, returning the most relevant episodes fragments to
  the user.

## license
Voilib is licensed under the GNU GPLv3 license. See [COPYING](./COPYING).

Permissions of this strong copyleft license are conditioned on making
available complete source code of licensed works and modifications,
which include larger works using a licensed work, under the same
license. Copyright and license notices must be preserved. Contributors
provide an express grant of patent rights.
