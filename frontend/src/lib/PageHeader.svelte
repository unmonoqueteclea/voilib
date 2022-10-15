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
      <a href="/pro" class="mr-5 hover:underline {selected == 2 ? 'font-bold' : ''}">
	{appname}
	<span class="badge badge-sm badge-primary badge-outline">PRO</span>
      </a>
    </nav>
    <a href="/pro">
      <button class="btn btn-outline gap-2 btn-sm invisible sm:visible">
	<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" class="w-5 h-5">
	  <path d="M9.25 13.25a.75.75 0 001.5 0V4.636l2.955 3.129a.75.75 0 001.09-1.03l-4.25-4.5a.75.75 0 00-1.09 0l-4.25 4.5a.75.75 0 101.09 1.03L9.25 4.636v8.614z" />
	  <path d="M3.5 12.75a.75.75 0 00-1.5 0v2.5A2.75 2.75 0 004.75 18h10.5A2.75 2.75 0 0018 15.25v-2.5a.75.75 0 00-1.5 0v2.5c0 .69-.56 1.25-1.25 1.25H4.75c-.69 0-1.25-.56-1.25-1.25v-2.5z" />
	</svg>
	Try your own media
      </button>
    </a>
  </div>
</header>
