<script>
  import AppLogo from '../AppLogo.svelte'
  import {appname} from '../app.js'
</script>
<main class="flex flex-col grow gap-12 lg:mt-6 px-8 mb-8  items-center">
  <div class="flex flex-col items-center">
    <h2 class="text-2xl font-bold max-w-2xl text-center">
      Text is not the only source of knowledge any more.
    </h2>
    <p class="mt-2 text-xl max-w-2xl text-center">
      <span class="font-medium">Voilib</span> has an army of monkeys
      trained to make audio content from multiple sources accessible
      for everyone. Check the list of <a class="underline"
      href="/content">episodes</a>.
    </p>
  </div>
  <div class="grid gap-12 grid-cols-1 xl:grid-cols-3 w-full lg:px-8">
    <!-- episode collection card -->
    <div class="card shadow-xl card-side">
      <figure>
	<img class="object-cover h-full w-28 md:w-44" src="/monkey-computer.jpg" alt="Monkey with laptop"/>
      </figure>
      <div class="card-body">
	<h2 class="card-title">Daily episode collection</h2>
	<p>Every morning, they <span class="font-semibold">collect</span> new episodes from multiple
     	  sources in English and in Spanish.
	</p>
      </div>
    </div>
    <!-- transcription card -->
    <div class="card w-full shadow-xl card-side">
      <figure>
	<img class="object-cover h-full w-28 md:w-44" src="/monkey-glasses.jpeg" alt="Monkey with headphones" />
      </figure>
      <div class="card-body">
	<h2 class="card-title">High quality transcriptions</h2>
	<p>
	  They listen, <span class="font-semibold">transcript</span> and store new episodes.
	</p>
      </div>
    </div>
    <!-- query card -->
    <div class="card w-full shadow-xl card-side">
      <figure>
	<img class="object-cover h-full w-28 md:w-44" src="/monkey-books.jpeg" alt="Monkey and a pile of books" />
      </figure>
      <div class="card-body">
	<h2 class="card-title">Smart search</h2>
	<p>
	  When you write a query, they will look for similar content
     	  in a huge pile of transcriptions. They understand <span class="font-semibold">natural
     	  language</span>!
	</p>
      </div>
    </div>
  </div>
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
