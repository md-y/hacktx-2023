<script>
	import Doughnut from '$components/Doughnut.svelte';
</script>

<div id="doughnut">
	<Doughnut
		data={{
			Car: 15000,
			'Desktop Computer': 2000,
			Laptop: 1000,
			iPad: 500,
			Custom: 5000
		}}
	/>
</div>

<style lang="scss">
	#doughnut {
		position: absolute;
		width: 30vw;
		height: 30vw;
		background-color: white;
	}
</style>
