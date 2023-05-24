import Home from './lib/pages/Home.svelte'
import Content from './lib/pages/Content.svelte'
import Query from './lib/pages/Query.svelte'
import About from './lib/pages/About.svelte'

export const routes = [
  {path: "/", component: Home},
  {path: "/query", component: Query},
  {path: "/about", component: About},
  {path: "/content", component: Content},
];

const routeMap = {
  "/": -1, "/query": 0, "/about": 1, "/content": 3
}

export function getPageNum(path) {
  return routeMap[path]
}

export function parseqs(ctx, next) {
  ctx.qs = new URLSearchParams(ctx.querystring);
  next();
}
