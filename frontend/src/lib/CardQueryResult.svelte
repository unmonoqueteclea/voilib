<script>
  export let result;

  import { createEventDispatcher } from 'svelte';
  const dispatch = createEventDispatcher();

  function secondsToTime(e){
    const h = Math.floor(e / 3600).toString().padStart(2,'0'),
          m = Math.floor(e % 3600 / 60).toString().padStart(2,'0'),
          s = Math.floor(e % 60).toString().padStart(2,'0');
    return h + ':' + m + ':' + s;
  }

  function badgeColor(r) {
    if (r.similarity<0.5) {
      return 'badge-error'
    } else if (r.similarity < 0.6) {
      return 'badge-warning'
    } else {
      return 'badge-success'
    }

  }

  $: episode = result.episode.episode;
  $: bColor = badgeColor(result);
  $: edate = new Date(result.episode.date);

  function click(){
    dispatch('click', {
      channel: result.channel,
      episode: result.episode,
      time: result.start
    });
  }
</script>

<div class="flex flex-col card h-auto bg-base-100 shadow-lg py-5 px-5">
  <div class="flex flex-row ml-2">
    <div class="avatar self-center" >
      <div class="w-20 h-20 rounded-full shadow-lg">
	<img src={result.channel.image} />
      </div>
    </div>
    <div class="flex flex-col ml-3">
      <a href={result.channel.url} target="_blank">
	<h3 class="text-lg font-bold">{result.channel.title}</h3>
      </a>
      <p class="text-sm">
	{result.episode.title}
	{#if episode != -1}
	  <span class="badge badge-sm badge-outline">Episode {episode}</span>
	{/if}
      </p>
      <div class="flex flex-row">
	<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" class="w-3 h-4 mr-1">
	  <path fill-rule="evenodd" d="M6.75 2.25A.75.75 0 017.5 3v1.5h9V3A.75.75 0 0118 3v1.5h.75a3 3 0 013 3v11.25a3 3 0 01-3 3H5.25a3 3 0 01-3-3V7.5a3 3 0 013-3H6V3a.75.75 0 01.75-.75zm13.5 9a1.5 1.5 0 00-1.5-1.5H5.25a1.5 1.5 0 00-1.5 1.5v7.5a1.5 1.5 0 001.5 1.5h13.5a1.5 1.5 0 001.5-1.5v-7.5z" clip-rule="evenodd" />
	</svg>
	<p class="text-xs text-slate-900">
	  { edate.toDateString() }
	</p>
      </div>
    </div>
  </div>
  <div class="flex mt-5">
    <p class="font-mono text-sm">
      <span>
	<div class="badge {bColor}">
	  <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" class="w-3 h-3 mr-1">
	    <path fill-rule="evenodd" d="M12.963 2.286a.75.75 0 00-1.071-.136 9.742 9.742 0 00-3.539 6.177A7.547 7.547 0 016.648 6.61a.75.75 0 00-1.152-.082A9 9 0 1015.68 4.534a7.46 7.46 0 01-2.717-2.248zM15.75 14.25a3.75 3.75 0 11-7.313-1.172c.628.465 1.35.81 2.133 1a5.99 5.99 0 011.925-3.545 3.75 3.75 0 013.255 3.717z" clip-rule="evenodd" />
	  </svg>
	  {Math.round(result.similarity*100)}%
	</div>
      </span>
      <span>
	<div class="badge pl-1">
	  <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-3 h-3 mr-1">
	    <path stroke-linecap="round" stroke-linejoin="round" d="M12 6v6h4.5m4.5 0a9 9 0 11-18 0 9 9 0 0118 0z" />
	  </svg>
	  {secondsToTime(result.start)}
	</div>
      </span>
      {result.text}...
    </p>
  </div>
  {#if result.channel.kind != "local"}
    <button class="mt-4 btn btn-sm btn-outline" on:click={click}>
      <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-5 h-5 mr-2">
	<path stroke-linecap="round" stroke-linejoin="round" d="M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
	<path stroke-linecap="round" stroke-linejoin="round" d="M15.91 11.672a.375.375 0 010 .656l-5.603 3.113a.375.375 0 01-.557-.328V8.887c0-.286.307-.466.557-.327l5.603 3.112z" />
      </svg>
      Play fragment
    </button>
  {:else}
    <div class="flex flex-row mt-6">
	<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-4 h-4 mr-1">
	  <path stroke-linecap="round" stroke-linejoin="round" d="M11.25 11.25l.041-.02a.75.75 0 011.063.852l-.708 2.836a.75.75 0 001.063.853l.041-.021M21 12a9 9 0 11-18 0 9 9 0 0118 0zm-9-3.75h.008v.008H12V8.25z" />
	</svg>
	<p class="text-xs text-slate-900">
	  Play fragment not available for local channels
	</p>
      </div>
  {/if}


</div>
