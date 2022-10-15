<script lang="js">
  export let unit = 'px';
  export let duration = '1.2s';
  export let size = '60';
  export let pause = false;

  const range = (size, startAt = 0) => [...Array(size).keys()].map((i) => i + startAt);  
  const durationUnitRegex = /[a-zA-Z]/;

  let durationUnit = duration.match(durationUnitRegex)?.[0] ?? 's';
  let durationNum = duration.replace(durationUnitRegex, '');
</script>
<div class="wrapper" style="--size: {size}{unit};  --duration: {duration}">
  {#each range(6, 1) as version}
    <div
      class="rect bg-neutral"
      class:pause-animation={pause}
      style="animation-delay: {(version - 1) * (+durationNum / 12)}{durationUnit}"
      />
    {/each}
  </div>
<style>
  .wrapper {
    height: var(--size);
    width: var(--size);
    display: inline-block;
    text-align: center;
    font-size: 10px;
  }
  .rect {
    height: 100%;
    width: 10%;
    display: inline-block;
    margin-right: 4px;
    transform: scaleY(0.4);
    animation: stretch var(--duration) ease-in-out infinite;
  }
  .pause-animation {
    animation-play-state: paused;
  }
  @keyframes stretch {
    0%,
    40%,
    100% {
      transform: scaleY(0.4);
    }
    20% {
      transform: scaleY(1);
    }
  }
</style>
