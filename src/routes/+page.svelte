<script>
	import Doughnut from '$components/Doughnut.svelte';
	import { numberWithCommas } from '$lib/util';
	import ArrowUp from '~icons/solar/double-alt-arrow-up-line-duotone';
	import ArrowDown from '~icons/solar/double-alt-arrow-down-line-duotone';

	const dailyChange = 69420;

	const changeDown = true;
</script>

<div class="col">
	<div class="row">
		<div id="money-text">
			<h1 class:red={changeDown}>
				{#if changeDown}
					<ArrowDown />
				{:else}
					<ArrowUp />
				{/if}
				${numberWithCommas(dailyChange.toString())}
			</h1>
			<h2>DAILY CHANGE</h2>
		</div>
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
	</div>
</div>

<style lang="scss">
	.col {
		display: flex;
		flex-direction: column;
		align-items: center;
		justify-content: center;
		height: 100%;
	}

	.row {
		display: flex;
		align-items: center;
		justify-content: space-between;
		max-width: 1000px;
		width: 100%;
		height: 30vh;

		background-color: #022842;

		padding: 10rem;
		border-radius: 5rem;
	}

	#doughnut {
		position: relative;
		width: 35rem;
		height: 35rem;
	}

	#money-text {
		font-size: 2rem;
		h1 {
			color: #00ce13;
			&.red {
				color: #ff3131;
			}
			margin: 0;
			display: flex;
			align-items: center;
		}

		h2 {
			margin: 0;
			font-family: 'Be Vietnam Pro', sans-serif;
			font-weight: 300;
			color: white;
		}
	}
</style>
