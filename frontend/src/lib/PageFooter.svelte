<script>
  import {appname} from './app.js'
    import AppLogo from './AppLogo.svelte'
</script>

<footer class="text-neutral text-xl font-medium ">
  <div class="flex flex-wrap flex-col sm:flex-row items-center sm:justify-center mb-5">
    <a class="items-center" href="/">
      <span class="ml-3 text-xl font-medium">{appname}</span>
    </a>
    <p class="flex text-sm text-gray-500 mt-1 ml-2">
      © 2023 Pablo González Carrizo <span class="invisible sm:visible ml-1">-</span></p>
    <a href="https://twitter.com/unmonoqueteclea" class="flex mt-1 text-sm text-gray-600 ml-1" rel="noopener noreferrer" target="_blank">
      @unmonoqueteclea
    </a>
  </div>
</footer>
