# Voilib - frontend documentation
Frontend of **Voilib**, based on [SvelteJS](https://svelte.dev/).

This project uses [SvelteJS](https://svelte.dev/) with
[Vite](https://vitejs.dev/) as the build tool. As client-side router,
it uses the tiny [page.js
library](https://github.com/visionmedia/page.js).

[TailwindCSS](https://tailwindcss.com/) classes and components from
[daisyUI](https://daisyui.com/) library are widely used in this
project.

**JavaScript Fetch API** is used to retrieved data from the backend.

ℹ️ Although you could run `npm run dev` to run the frontend locally, I
really encourage you to use the provided Docker configuration. Read
very carefully the main [readme](../readme.md) and the [deployment
docs](../infra/readme.md) and run the `development` configuration
provided the [infra/ folder](../infra/). You will find there
instructions to run all the app services using Docker and the needed
commands to start populating the application with content. As code is
mounted, you won't need to restart/rebuild containers when you do
changes. Your changes will be applied automatically, as Svelte
supports hot reload.
