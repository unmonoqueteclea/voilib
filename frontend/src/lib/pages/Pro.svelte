<script>
import { onMount } from "svelte";
import {API_URL} from '../../api.js'
let email;
let lastUserCreated = false;
let error = false;

async function createIntUser() {
  let url = new URL(API_URL + "/users/interested")
  let data = {email: email}
    const resp = await fetch(url, {
      method: 'POST',
      body: JSON.stringify(data),
      headers: {"content-type": "application/json"}
    })
  if (resp.status == 200) {
    lastUserCreated = email
    error = false
  } else if (resp.status == 400) {
      error = (await resp.json()).detail
      lastUserCreated = email
  }
      return
}

</script>
<main class="flex flex-col grow place-content-center pb-12" >
    <div class="container m-auto px-6 md:py-6 md:px-12 lg:px-20">
        <div class="m-auto text-center w-4/5 lg:w-9/12 xl:w-9/12">
          <h2 class="text-xl lg:text-2xl font-bold">
	    Do you want to transcript and index your own content?
	  </h2>
        </div>
        <div class="mt-12 m-auto items-center justify-center md:flex md:space-y-0 md:-space-x-4 xl:w-10/12">
            <div class="relative z-10 -mx-4 group md:w-6/12 md:mx-0 lg:w-6/12">
                <div aria-hidden="true" class="absolute top-0 w-full h-full rounded-2xl bg-white shadow-xl transition duration-500 group-hover:scale-105 lg:group-hover:scale-110"></div>
                <div class="relative p-6 space-y-6 lg:p-8">
                    <h3 class="text-3xl text-gray-700 font-semibold text-center">Voilib <span class="text-primary">PRO</span></h3>
                    <ul role="list" class="w-max space-y-4 py-2 m-auto text-gray-600">
                        <li class="space-x-2">
                            <span class="text-purple-500 font-semibold">🎧</span>
                            <span>For content creators</span>
                        </li>
                        <li class="space-x-2">
                            <span class="text-purple-500 font-semibold">🏫</span>
                            <span>For online teachers or students</span>
                        </li>
                        <li class="space-x-2">
                            <span class="text-purple-500 font-semibold">🎤</span>
                            <span>For journalists </span>
                        </li>
			<li class="space-x-2">
                            <span class="text-purple-500 font-semibold">🏢</span>
                            <span>For small and big companies </span>
                        </li>
			<li class="space-x-2">
                            <span class="text-purple-500 font-semibold">💰</span>
                            <span>From 50 USD/month </span>
                        </li>
                    </ul>
		    {#if !error &&  (lastUserCreated && lastUserCreated == email)}
		      <div class="flex flx-row place-content-center mt-2">
			<div class="alert alert-success text-white shadow-lg w-full">
			  <div>
			    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
			      <path stroke-linecap="round" stroke-linejoin="round" d="M9 12.75L11.25 15 15 9.75M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
			    </svg>
			    <div>
			      <h3 class="font-bold">Email registered succesfully</h3>
			      <div class="text-xs">
				A Voilib admin will contact you soon
				(2/3 days).
			      </div>
			    </div>
			  </div>
			</div>
		      </div>
		    {/if}
		    {#if error &&  (lastUserCreated && lastUserCreated == email)}
		      <div class="flex flx-row place-content-center mt-2">
			<div class="alert alert-error text-white shadow-lg w-full">
			  <div>
			    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
			      <path stroke-linecap="round" stroke-linejoin="round" d="M9 12.75L11.25 15 15 9.75M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
			    </svg>
			    <div>
			      <h3 class="font-bold">Error while registering email</h3>
			      <div class="text-xs">{error}</div>
			    </div>
			  </div>
			</div>
		      </div>
		    {/if}
		    <div class="flex flex-row place-content-center">
		      <input
			type="email"
			placeholder="Enter your email"
			bind:value="{email}"
			class="textarea textarea-bordered w-full h-16 text-lg"
			/>
		    </div>
		    <div class="flex flx-row place-content-center mt-5">
		      <button on:click="{createIntUser}" class="btn w-full">
			<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6 mr-4">
			  <path stroke-linecap="round" stroke-linejoin="round" d="M2.25 13.5h3.86a2.25 2.25 0 012.012 1.244l.256.512a2.25 2.25 0 002.013 1.244h3.218a2.25 2.25 0 002.013-1.244l.256-.512a2.25 2.25 0 012.013-1.244h3.859m-19.5.338V18a2.25 2.25 0 002.25 2.25h15A2.25 2.25 0 0021.75 18v-4.162c0-.224-.034-.447-.1-.661L19.24 5.338a2.25 2.25 0 00-2.15-1.588H6.911a2.25 2.25 0 00-2.15 1.588L2.35 13.177a2.25 2.25 0 00-.1.661z" />
			</svg>
			I am interested
		      </button>
		    </div>
                </div>
            </div>
            <div class="relative group md:w-6/12 lg:w-7/12">
                <div aria-hidden="true" class="absolute top-0 w-full h-full rounded-2xl bg-white shadow-lg transition duration-500 group-hover:scale-105"></div>
                <div class="relative p-8  md:pl-12 md:rounded-r-2xl lg:pl-20 lg:p-8">
                  <ul role="list" class="space-y-4 py-2 text-gray-600">
		    <li class="space-x-2">
                            <span class="text-purple-500 font-semibold">&check;</span>
                            <span>Upload your own public or private content</span>
                        </li>
                        <li class="space-x-2">
                            <span class="text-purple-500 font-semibold">&check;</span>
                            <span>Complete transcriptions, synchronized with audio</span>
                        </li>
			<li class="space-x-2">
                            <span class="text-purple-500 font-semibold">&check;</span>
                            <span>20+ languages available</span>
                        </li>
                        <li class="space-x-2">
                            <span class="text-purple-500 font-semibold">&check;</span>
                            <span>Auto-generated summaries</span>
                        </li>
			<li class="space-x-2">
                            <span class="text-purple-500 font-semibold">&check;</span>
                            <span>Share content privately with your followers</span>
                        </li>
                    </ul>
                  <p class="text-gray-700 mt-6">
		    ℹ️ You will have your private version of <span class="font-semibold">Voilib</span> with
		    your own content that you can share with your followers.
		  </p>
                </div>
            </div>
        </div>
    </div>

</main>
