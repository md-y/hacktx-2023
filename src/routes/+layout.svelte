<script>
	import 'carbon-components-svelte/css/white.css';
	import { onMount} from 'svelte';
	import { user, authToken} from '../lib/store.js'
	import { getDoughnutData } from '$lib/assets.js';

	async function getData() {
		try {
			let at = $authToken;
			let response = await fetch('https://helloworld-feagyby2hq-uc.a.run.app/user', {
				headers: {
					AuthToken: at
				}
			});
			let userData = await response.json();
			$user = userData;
		} catch (error) {
			console.log(error);
		}
	}

	onMount(async ()=>{
		await getData();
	})
</script>

<div id="bg">
	<slot />
</div>

<svelte:head>
	<link
		rel="stylesheet"
		href="https://fonts.googleapis.com/css?family=Roboto:regular,bold|Be+Vietnam+Pro:Light,regular,bold&display=swap"
	/>
</svelte:head>

<style lang="scss">
	:global(body) {
		margin: 0;
	}

	:global(p),
	:global(h1),
	:global(h2),
	:global(h3),
	:global(h4),
	:global(h5),
	:global(h6) {
		font-family: 'Be Vietnam Pro', sans-serif;
	}

	#bg {
		height: 100vh;
		width: 100vw;
		background-color: #085e7d;
	}
</style>
