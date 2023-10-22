<script>
	import AssetBarGraph from '$components/AssetBarGraph.svelte';
	import BackIcon from '~icons/material-symbols/arrow-back';
</script>

<a id="back-button" href="/"><BackIcon /></a>
<div id="graph-container">
	<AssetBarGraph />
</div>

<style lang="scss">
	#back-button {
		position: absolute;
		z-index: 100;
		top: 2rem;
		left: 2rem;

		:global(svg) {
			color: white;
			font-size: 2rem;
		}
	}

	#graph-container {
		position: absolute;
		inset: 0;
		padding: 4rem;
		padding-bottom: 0;
		overflow-y: auto;

		background-color: #022842;

		& :global(canvas) {
			width: 100%;
			height: 1000vh;
		}
	}
</style>
