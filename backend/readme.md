# voilib - back-end

Python project with the back-end and API of `voilib`.

Install the project with the usual `pip install .`. You can also do
`pip install -e .[dev]` to ensure you install it in editable mode and
including development dependencies.

For tests copy .env.example to .env

## quickstart
To run the whole project (not just the back-end) using `Docker`
containers see [main project readme](../readme.md). However, if you
just want to run the back-end locally, do `make start`. After that,
you will find `swagger` in [0.0.0.0:8080/docs](http://0.0.0.0:8080/docs).

The same [makefile](./makefile) contains other targets for common
tasks such as creating migrations or applying them. Run `make` to see
all the available targets.

Run `make migrate` to ensure all the needed database tables are
created.

## scripts
The package incldue some scripts to do some common tasks such updating
episodes from the list of feeds or transcribing episodes from the last
X days. All of them are defined in `[options.entry_points]` in
[setup.cfg](./setup.cfg) file. You can use `--help` to see all their
information, e.g. `voilib-checks --help`.

## settings
All the application settings are in
[settings.py](./src/voilib/settings.py).  That module contains default
values for all the settings (usually used when running the application
locally, without Docker).

In Docker-based deployments, those settings will be usually taken from
environment variables.

You can use settings like this:

```python
from voilib.settings import settings

print(settings.redis_host)
```
