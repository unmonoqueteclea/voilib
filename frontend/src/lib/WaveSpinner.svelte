<script>
  export let color = '#FFFFFF';
  export let unit = 'px';
  export let duration = '1.25s';
  export let size = '100';
  export let pause = false;
  const range = (size, startAt = 0) => [...Array(size).keys()].map((i) => i + startAt);  
  const durationUnitRegex = /[a-zA-Z]/;
  let durationUnit = duration.match(durationUnitRegex)?.[0] ?? 's';
  let durationNum = duration.replace(durationUnitRegex, '');
</script>
<div class="wrapper" style="--size: {size}{unit}; --color: {color}; --duration: {duration};">
	{#each range(10, 0) as version}
	  <div
	    class="bar"
	    class:pause-animation={pause}
	    style="left: {version * (+size / 5 + (+size / 15 - +size / 100)) +
		   unit}; animation-delay: {version * (+durationNum / 8.3)}{durationUnit};"
	    />
	  {/each}
	</div>
<style>
  .wrapper {
    position: relative;
    display: flex;
    justify-content: center;
    align-items: center;
    width: calc(var(--size) * 2.5);
    height: var(--size);
    overflow: hidden;
  }
  .bar {
    position: absolute;
    top: calc(var(--size) / 10);
    width: calc(var(--size) / 5);
    height: calc(var(--size) / 10);
    margin-top: calc(var(--size) - var(--size) / 10);
    transform: skewY(0deg);
    background-color: var(--color);
    animation: motion var(--duration) ease-in-out infinite;
  }
  .pause-animation {
    animation-play-state: paused;
  }
  @keyframes motion {
    25% {
      transform: skewY(25deg);
    }
    50% {
      height: 100%;
      margin-top: 0;
    }
    75% {
      transform: skewY(-25deg);
    }
  }
</style>
