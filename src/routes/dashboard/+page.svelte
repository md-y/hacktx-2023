<script lang="ts">
	import Doughnut from '$components/Doughnut.svelte';
	import { formatNumber } from '$lib/util.js';
	import ArrowUp from '~icons/solar/double-alt-arrow-up-line-duotone';
	import ArrowDown from '~icons/solar/double-alt-arrow-down-line-duotone';
	import Graph from '$components/Graph.svelte';
	import NewAssetModal from '$components/NewAssetModal.svelte';
	import { getDoughnutData, getNetWorth } from '$lib/assets';
	import _ from 'lodash';
	import { TooltipIcon } from 'carbon-components-svelte';
	import BrowseAssetsIcon from '~icons/material-symbols/insert-chart-outline';
	import AddAssetIcon from '~icons/material-symbols/add-rounded';
	import { base } from '$app/paths';
	import {signOut} from 'firebase/auth';
    import {auth} from '../../lib/util.js';
	import { goto } from '$app/navigation';

	let todayAssetData = getDoughnutData();
	let todayNetWorth = _.sum(Object.values(todayAssetData));
	let yesterdayAssetData = getNetWorth(Date.now() - 24 * 60 * 60 * 1000);
	let lastMonthAssetData = getNetWorth(Date.now() - 24 * 60 * 60 * 1000 * 30);
	let dailyChange = todayNetWorth - yesterdayAssetData;
	let monthlyChange = todayNetWorth - lastMonthAssetData;

	const DAY = 24 * 60 * 60 * 1000;

	let openModal = false;

	function logout(){
		signOut(auth); 
		goto('/');
	}

</script>

<NewAssetModal bind:open={openModal} />

<div class="main-card">
	<div class="row">
		<div class="icons">
			<h1>Am I Broke?</h1>
			
			<a on:click={() => (openModal = true)}>
				<TooltipIcon icon={AddAssetIcon} tooltipText={'Add new asset'} />
			</a>
			<a href="{base}/assets">
				<TooltipIcon icon={BrowseAssetsIcon} tooltipText={'Browse all assets'} />
			</a>
			<button on:click={logout}>Logout</button>
		</div>
		<div class="money-text">
			<h1 class:red={dailyChange < 0} class:green={dailyChange > 0}>
				{#if dailyChange < 0}
					<ArrowDown />
				{:else}
					<ArrowUp />
				{/if}
				${formatNumber(dailyChange)}
			</h1>
			<h2>DAILY CHANGE</h2>
		</div>
		<div class="money-text">
			<h1 class:red={monthlyChange < 0} class:green={monthlyChange > 0}>
				{#if monthlyChange < 0}
					<ArrowDown />
				{:else}
					<ArrowUp />
				{/if}
				${formatNumber(monthlyChange)}
			</h1>
			<h2>MONTHLY CHANGE</h2>
		</div>
		<div id="doughnut">
			<Doughnut data={todayAssetData} />
		</div>
	</div>
	<div class="row">
		<div id="net-worth-graph">
			<h1>NET WORTH</h1>
			<Graph
				xValues={[-365, 0, 1]}
				yValues={(v) => getNetWorth(Date.now() + v * DAY)}
				startDate={new Date(Date.now() - 365 * DAY)}
			/>
		</div>
	</div>
</div>

<style lang="scss">
	$doughnut-width: 35rem;
	$big-text: 6vmin;
	$smaller-text: 4vmin;
	$trans-duration: 1s;

	.main-card {
		position: absolute;
		top: 5vh;
		bottom: 5vh;
		left: 5vw;
		right: 5vw;
		background-color: #022842;
		border-radius: 2rem;
		filter: drop-shadow(2px 2px 2px #000000);

		display: flex;
		flex-direction: column;

		padding-left: 4vw;
		padding-right: 4vw;
		padding-top: 2vh;
		padding-bottom: 2vh;
	}

	.row {
		width: 100%;
		display: flex;
		align-items: center;
		justify-content: space-between;
		gap: 2rem;
	}

	.icons {
		position: absolute;
		left: 4vw;
		top: 4vw;
		width: 100%;

		display: flex;
		gap: 1rem;
		align-items: center;

		h1 {
			color: white;
			font-weight: 400;
			font-size: $big-text * 1.25;
			margin-right: 2rem;
		}

		:global(svg) {
			color: white;
			font-size: 3rem;
			transition: scale 0.25s;
		}

		:hover {
			:global(svg) {
				scale: 115% 115%;
			}
		}
	}

	#net-worth-graph {
		width: 100%;
		height: 25vh;
		animation: fadeIn $trans-duration;

		h1 {
			color: white;
			font-size: $smaller-text;
			translate: 0px -1rem;
		}
	}

	#doughnut {
		position: relative;
		width: 30vw;
		height: 30vw;
	}

	.money-text {
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