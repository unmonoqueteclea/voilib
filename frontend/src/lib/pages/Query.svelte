<script>
  import { onMount } from "svelte";
  import CardQueryResult from '../CardQueryResult.svelte'
  import Player from '../Player.svelte'
  import StretchSpinner from '../StretchSpinner.svelte'
  import {API_URL} from '../../api.js'
  export let qs;

  // receive query from url
  let query = qs.get("q")
  let queryLoading = false;
  let queryResults;

  let player;

  async function doQuery(query) {
    if (query.length > 0) {
      queryLoading = true
      queryResults = false;
      history.replaceState(history.state, "", "?q=" + query);
      let url = new URL(API_URL + "/media/query")
      let params = {query_text: query, k: 6}
      Object.keys(params).forEach(key => url.searchParams.append(key, params[key]))
      await fetch(url).then(r => r.json()).then(data => {queryResults = data;});
      queryLoading = false
    }
  }

  onMount(async () => {if (query) {await doQuery(query)}})

  let episodePlay;
  let channelPlay;
  let time;

  function click(data) {
    episodePlay = data.detail.episode
    channelPlay = data.detail.channel
    time = data.detail.time
    setTimeout(() => {
      player.scrollIntoView()
    }, 50)
  }

  function goToQuery(event) {
    if (event.key == 'Enter') {
      event.stopPropagation();
      event.preventDefault();
      doQuery(query)
    }
  }

  $: maxSim = queryResults ? queryResults[0].similarity : 1

</script>

<main class="flex flex-col grow pb-12 mt-6">
  <div class="grid grid-cols-1 md:grid-cols-3 mx-5 md:mx-16 gap-4">
    <textarea
      placeholder="Write your query..."
      class="textarea textarea-bordered h-16 text-lg md:col-span-2"
      bind:value={query}
      on:keypress={goToQuery}
      rows="1"
    />
    <button class="btn h-16" on:click={doQuery(query)}>
      <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6 mr-2">
	<path stroke-linecap="round" stroke-linejoin="round" d="M15.362 5.214A8.252 8.252 0 0112 21 8.25 8.25 0 016.038 7.048 8.287 8.287 0 009 9.6a8.983 8.983 0 013.361-6.867 8.21 8.21 0 003 2.48z" />
	<path stroke-linecap="round" stroke-linejoin="round" d="M12 18a3.75 3.75 0 00.495-7.467 5.99 5.99 0 00-1.925 3.546 5.974 5.974 0 01-2.133-1A3.75 3.75 0 0012 18z" />
      </svg>
      Search content
    </button>
  </div>
  <div class="flex flex-row mt-6 mx-5 md:mx-16 text-gray-500">
    ℹ️ Voilib will find related content in episodes
    transcriptions. Trying to find specific poscast titles or episodes
    names won't be useful.
  </div>
  <div class="flex flex-row mt-2 mx-5 md:mx-16 text-gray-500">
    📢  We are happy to receive your feedback
    <a class="underline ml-1" href="mailto: unmonoqueteclea@gmail.com"> here</a>!
  </div>

  <div class="flex flex-row mt-2 mx-5 md:mx-16 text-gray-500">
    ✅ <strong class="ml-2">New episodes added on April, 7th)</strong>. More than 1K hours of episodes indexed!
  </div>

  <div class="flex flex-row place-content-center mt-1 mx-5 md:mx-16">
    <div class="divider w-full"></div>
  </div>
  {#if maxSim < 0.55}
  <div class="flex flex-row mt-2 mb-2 mx-5 md:mx-16 text-gray-500 font-semibold">
    🚩Low similarity scores, results may not be relevant. We add new
    episodes every day, try again in a few days.
  </div>
  {/if}
  {#if channelPlay}
    <div  bind:this="{player}" class="flex flex-row place-content-center mt-1 mx-5 md:mx-10">
      <Player time={time} channel={channelPlay} episode={episodePlay}/>
    </div>
  {/if}
  {#if queryResults}
    <div class="flex flex-row mt-10 mx-10">
      <div class="grid gap-4 grid-cols-1 md:grid-cols-2 lg:grid-cols-3 w-full">
	{#each queryResults as result }
	  <CardQueryResult  on:click={click} result={result} />
	{/each}
      </div>
    </div>
  {:else if queryLoading}
    <div class="flex flex-col grow items-center justify-center">
      <StretchSpinner size=100/>
      <p class="mt-8 text-lg">Searching related content...</p>
    </div>
  {:else}
    <div class="flex flex-col grow items-center justify-center text-center">
      <p class="lg:text-xl text-center text-gray-500">
	Write your <span class="font-semibold">query</span> in English
	🇺🇸 or Spanish 🇪🇸
      </p>
      <p class="lg:text-xl mt-2 text-gray-500">
	Related episodes fragments will appear here
      </p>
    </div>
  {/if}
</main>
