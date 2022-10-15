# voilib infrastructure
This folder contains all the infrastructure code needed to run
**Voilib**.  It uses some `Docker`-based services configured with a
`Docker Compose` file (that is different in development and in
production).

The main commands to build and run all the needed services are in
`makefile`, run `make` to see all of them.

## development
In development, `frontend` and `backend` code is using a `bind mount`
so that you don't need to rebuild the images every time you change
something there.

The `compose` file expects an `env` file, in the
[development](./development) folder, with the name `.env.dev`.  **You
should create it before building any service**, you can copy the
provided [.env.dev.example](./development/.env.dev.example).

When the `.env.dev` file is created, you can build all the services
images with `make dev-build` or run all of them with `make dev-run`.

The following services will be available:
    - **Voilib** app frontend at `http://localhost`
	- `API` at `http://localhost/service/` with `swagger` at `http://localhost/service/docs`
	- `Traefik` dashboard at `http://localhost:8080`
	- `RQ Monitor`, to monitor asynchronous tasks, at
      `http://localhost:8899`

## production
As in development, you should create the `.env.prod` file from the
provided [.env.prod.example](./production/.env.prod.example). When you
do it, ensure to use your domain for `VITE_API_HOST` and change it
also in the following line from the `compose.yml` file:

```yaml
- "traefik.http.routers.ui.rule=(Host(`voilib.com`) && PathPrefix(`/`))"
```

As with development, You have `make prod-build` and `make prod-run`
`make` targets available.
