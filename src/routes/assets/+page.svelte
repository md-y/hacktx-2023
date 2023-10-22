<script>
	import { base } from '$app/paths';
	import AssetBarGraph from '$components/AssetBarGraph.svelte';
	import BackIcon from '~icons/material-symbols/arrow-back';
	import { page } from '$app/stores';
	import { onMount } from 'svelte';

	/**
	 * @type {string | null | undefined}
	 */
	let assetType = undefined;
	onMount(() => {
		assetType = $page.url.searchParams.get('type');
	});
</script>

<a id="back-button" href="{base}/dashboard"><BackIcon /></a>
<div id="graph-container">
	{#key assetType}
		<AssetBarGraph focusType={assetType ?? undefined} />
	{/key}
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
		}
	}
</style>
