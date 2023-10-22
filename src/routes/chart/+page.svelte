<script>
	import Graph from '$components/Graph.svelte';
</script>

<div>
	<Graph xValues={[0, 100, 1]} yValues={(v) => v * v} />
</div>

<style lang="scss">
	div {
		width: 100vw;
		height: 100vh;
	}
</style>
