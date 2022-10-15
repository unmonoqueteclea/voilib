<script>
  import page from "page";

  const QUERIES = [
    "e.g. How is AI going to change the world?      ",
    "e.g. Ways to fight climate change       ",
    "e.g. what are the best cities to live in?     ",
    "e.g. what are the best ways to burn fat fast?     ",
    "e.g. How long will inflation last in America?     ",
    "e.g. what is the future of Twitter?     ",
    "e.g. last advances in AI     ",
    "e.g. What are the benefits of fasting?      ",
    "e.g. should I sell my Bitcoins?     "
]
let queryNum = 0;
let queryEnd = 0;
let shown = ""
let queryText = ""
$: href = "/query?q="+queryText

function typeIteration() {
  const current = QUERIES[queryNum];
  if (shown.length < current.length) {
    queryEnd += 1;
  } else {
    queryEnd = 0
    if ((queryNum + 1) < QUERIES.length) {
      queryNum += 1
    } else {
      queryNum = 0
    }
  }
  shown = QUERIES[queryNum].slice(0, queryEnd);
}

  setInterval(typeIteration, 60);

  function goToQuery(event) {
    if (event.key == 'Enter') {
      page.redirect(href)
    }
  }
</script>

<section class="query text-center px-8">
  <div>
    <textarea
      class="textarea textarea-bordered max-w-3xl w-full text-lg"
      placeholder={shown}
      bind:value={queryText}
      on:keypress={goToQuery}/>
  </div>
  <a {href}>
    <button class="btn btn-block max-w-3xl mt-4">
    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6 mr-2">
      <path stroke-linecap="round" stroke-linejoin="round" d="M15.362 5.214A8.252 8.252 0 0112 21 8.25 8.25 0 016.038 7.048 8.287 8.287 0 009 9.6a8.983 8.983 0 013.361-6.867 8.21 8.21 0 003 2.48z" />
      <path stroke-linecap="round" stroke-linejoin="round" d="M12 18a3.75 3.75 0 00.495-7.467 5.99 5.99 0 00-1.925 3.546 5.974 5.974 0 01-2.133-1A3.75 3.75 0 0012 18z" />
    </svg>
    Search content
  </button>
  </a>
</section>
