<script>
  import { onMount } from "svelte";
  import {API_URL} from '../../api.js'
  import StretchSpinner from '../StretchSpinner.svelte'
  let queryLoading = false;
  let queryResults = [];

  async function doQuery() {
    queryLoading = true
    queryResults = [];
    let url = new URL(API_URL + "/analytics/media-count")
    await fetch(url).then(r => r.json()).then(data => {queryResults = data.channels;});
    queryLoading = false
  }

  $: channels = queryResults.filter((c) => c.available_episodes > 0);

  onMount(async () => {await doQuery()})
</script>
<main class="flex flex-col grow gap-12 lg:mt-6 px-8 mb-8  items-center">
  <div class="flex flex-col items-center">
    <h2 class="text-2xl font-bold max-w-2xl text-center">
      🎧 These are all the podcasts available
    </h2>
    <p class="mt-2 text-xl max-w-2xl text-center">
      The list grows every day!
    </p>
  </div>
  {#if channels.length > 0}
    <div class="grid gap-12 grid-cols-1 md:grid-cols-2 xl:grid-cols-3 w-full lg:px-8">
      <!-- episode collection card -->
      {#each channels as channel}
	<div class="card shadow-xl card-side">
	  <figure>
	    <img class="object-fit h-full w-28 md:w-44" src="{channel.image}" />
	  </figure>
	  <div class="card-body">
	    <a href="{channel.url}">
	      <h2 class="line-clamp-3 card-title text-base">{channel.title}</h2>
	    </a>
	    <p><span class="font-semibold">{channel.available_episodes}</span> episodes available.
	    </p>
	  </div>
	</div>
      {/each}
    </div>
  {:else}
    <div class="flex flex-col grow items-center justify-center">
      <StretchSpinner size=60/>
    </div>
  {/if}
  <div>
    <p class="mt-6  max-w-2xl text-center">
      ℹ️ Do you want to index your own content? Are you a content creator
      and want to offer full transcriptions and automatically
      generated summaries to your subscribers?
    </p>
    <p class="mt-2 max-w-2xl text-center">
      Check <a class="ml-1 underline" href="/pro">Voilib PRO</a>.
    </p>
  </div>

</main>
