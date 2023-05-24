<script>
import {appname} from './app.js'
import AppLogo from './AppLogo.svelte'
export let selected;
</script>

<header class="text-neutral">
  <div class="flex flex-wrap p-5 flex-col sm:flex-row items-center">
    <a href="/" class="flex items-center mb-4 sm:mb-0">
      <AppLogo />
      <span class="ml-2 text-xl font-medium ">{appname}</span>
    </a>
    <nav class="sm:mr-auto sm:ml-4 sm:py-1 sm:pl-4 sm:border-l sm:border-neutral flex flex-wrap">
      <a href="/query" class="mr-5 hover:underline {selected == 0 ? 'font-bold' : ''}">
	Query
      </a>
      <a href="/about" class="mr-5 hover:underline {selected == 1 ? 'font-bold' : ''}">
	About
      </a>
    </nav>
  </div>
</header>
