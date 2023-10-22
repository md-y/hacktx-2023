<script lang="ts">
	import Doughnut from '$components/Doughnut.svelte';
	import { formatNumber } from '$lib/util.js';
	import ArrowUp from '~icons/solar/double-alt-arrow-up-line-duotone';
	import ArrowDown from '~icons/solar/double-alt-arrow-down-line-duotone';
	import Graph from '$components/Graph.svelte';
	import NewAssetModal from '$components/NewAssetModal.svelte';
	import { getDoughnutData } from '$lib/assets';

	const dailyChange = 69420;

	let assetData = getDoughnutData();

	let changeDown: boolean = false;
</script>

<div class="main-card">
	<div class="row">
		<div id="money-text">
			<h1 class:red={changeDown} class:green={!changeDown}>
				{#if changeDown}
					<ArrowDown />
				{:else}
					<ArrowUp />
				{/if}
				${formatNumber(dailyChange)}
			</h1>
			<h2>DAILY CHANGE</h2>
		</div>
		<div id="doughnut">
			<Doughnut data={assetData} />
		</div>
	</div>
	<div class="row">
		<div id="net-worth-graph">
			<h1>NET WORTH</h1>
			<Graph xValues={[0, 100, 1]} yValues={(v) => v * v} />
		</div>
	</div>
</div>

<style lang="scss">
	$card-padding: 4rem;
	$x-padding: 8rem;
	$doughnut-width: 35rem;
	$big-text: 4rem;
	$smaller-text: 2.5rem;
	$trans-duration: 1s;

	.main-card {
		position: absolute;
		inset: $card-padding;
		background-color: #022842;
		border-radius: 2rem;
		filter: drop-shadow(2px 2px 2px #000000);

		display: flex;
		flex-direction: column;
	}

	.row {
		width: 100%;
		display: flex;
		align-items: center;
		justify-content: space-between;

		padding-left: $x-padding;
		padding-right: $x-padding;
	}

	#net-worth-graph {
		width: 100%;
		height: calc(100vh - $card-padding * 3 - $doughnut-width - $smaller-text);
		animation: fadeIn $trans-duration;

		h1 {
			color: white;
			font-size: $smaller-text;
			translate: 0px -1rem;
		}
	}

	#doughnut {
		position: relative;
		width: $doughnut-width;
		height: $doughnut-width;
	}

	#money-text {
		h1 {
			color: white;
			font-size: $big-text;

			&.green {
				color: #00ce13;

				:global(svg) {
					animation: slideIn $trans-duration * 1.5;
				}

				@keyframes slideIn {
					0% {
						opacity: 0;
						translate: 0 -10px;
					}
					100% {
						opacity: 1;
						translate: 0px 0px;
					}
				}
			}
			&.red {
				color: #ff3131;

				:global(svg) {
					animation: slideIn $trans-duration * 1.5;
				}

				@keyframes slideIn {
					0% {
						opacity: 0;
						translate: 0 10px;
					}
					100% {
						opacity: 1;
						translate: 0px 0px;
					}
				}
			}
			margin: 0;
			display: flex;
			align-items: center;

			transition: color $trans-duration;
			animation: slideLeft $trans-duration;
		}

		h2 {
			margin: 0;
			color: white;
			font-size: $smaller-text;

			animation: slideRight $trans-duration;
		}
	}

	@keyframes slideRight {
		0% {
			opacity: 0;
			translate: -10px 0px;
		}
		100% {
			opacity: 1;
			translate: 0px 0px;
		}
	}

	@keyframes slideLeft {
		0% {
			opacity: 0;
			translate: 10px 0px;
		}
		100% {
			opacity: 1;
			translate: 0px 0px;
		}
	}

	@keyframes fadeIn {
		0% {
			opacity: 0;
		}
		100% {
			opacity: 1;
		}
	}
</style>
