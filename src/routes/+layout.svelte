<div id="bg">
	<slot />
</div>

<svelte:head>
	<link
		rel="stylesheet"
		href="https://fonts.googleapis.com/css?family=Roboto:regular,bold&display=swap"
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
		font-family: 'Roboto', sans-serif;
	}

	#bg {
		height: 100vh;
		width: 100vw;
		background-color: #085e7d;
	}
</style>
