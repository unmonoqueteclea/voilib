<script>
  import router from "page"
  import {routes, parseqs, getPageNum} from "./routes.js";
  import PageHeader from './lib/PageHeader.svelte'
  import PageFooter from './lib/PageFooter.svelte'

  // routing configuration
  let pagenum = -1;
  let page;
  let qs;

  router('*', parseqs)
  routes.forEach(route => {
    router(
      route.path,
      (ctx, next) => {
	pagenum = getPageNum(ctx.pathname);
	qs = ctx.qs;
	next();
      },
      () => {page = route.component;}
    );
  });
  router.start();
</script>

<div class="flex flex-col min-h-screen">
  <PageHeader selected={pagenum} />
  <svelte:component this={page} qs={qs}/>
  <PageFooter/>
</div>
