<script>
  import {AudioPlayer, isPlaying, PlayIcon} from 'svelte-mp3';
  import WaveSpinner from './WaveSpinner.svelte'

  export let channel;
  export let episode;
  export let time;

  let audio = {};
  let isWaiting = false

  $: {
    isWaiting = episode;
    durationChanged(null)
  }

  $: edate = new Date(episode.date);
  $: eurl = [episode.url];


  function canplay(event) {
    isWaiting = false
    isPlaying.set(true)
  }
  function durationChanged(event) {
    localStorage.setItem('volume', 1)
    isPlaying.set(false)
    audio.currentTime = time;
    isPlaying.set(true)
  }
</script>
<div class="card w-full h-80 sm:h-64 lg:h-40 bg-base-100 shadow-xl image-full">
  <img class="object-cover w-full h-full" src="{channel.image}"  />
  <div class="grid grid-cols-2 lg:grid-cols-3 card-body">
    <div class="col-span-2 flex flex-col">
      <h2 class="card-title line-clamp-1">{ channel.title }</h2>
      <p class="max-h-32 line-clamp-3">{episode.title}</p>
      <div class="flex flex-row mt-0">
	<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" class="w-5 h-5 mr-1 mt-2">
	  <path fill-rule="evenodd" d="M6.75 2.25A.75.75 0 017.5 3v1.5h9V3A.75.75 0 0118 3v1.5h.75a3 3 0 013 3v11.25a3 3 0 01-3 3H5.25a3 3 0 01-3-3V7.5a3 3 0 013-3H6V3a.75.75 0 01.75-.75zm13.5 9a1.5 1.5 0 00-1.5-1.5H5.25a1.5 1.5 0 00-1.5 1.5v7.5a1.5 1.5 0 001.5 1.5h13.5a1.5 1.5 0 001.5-1.5v-7.5z" clip-rule="evenodd" />
	</svg>
	<p class="text-md mt-1 ml-1">
	  { edate.toDateString() }
	</p>
      </div>
    </div>
    <div class="mx-8 col-span-2 mt-5 lg:mt-0 lg:col-span-1">
      {#if isWaiting}
      <WaveSpinner size=80/>
      {/if}
      <AudioPlayer
	class="{ isWaiting ? 'invisible' : 'visible'}"
	color="white"
	showNext="{false}"
	showPrev="{false}"
	showShuffle="{false}"
	showTrackNum="{false}"
	disableVolSlider="{true}"
	urls={eurl}
	bind:audio={audio}
	on:canplay={canplay}
	on:canplaythrough={canplay}
	on:durationchange={durationChanged}
	/>
    </div>
  </div>
</div>
