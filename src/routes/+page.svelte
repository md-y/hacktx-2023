<script lang="ts">
	import Doughnut from '$components/Doughnut.svelte';
	import { numberWithCommas } from '$lib/util';
	import ArrowUp from '~icons/solar/double-alt-arrow-up-line-duotone';
	import ArrowDown from '~icons/solar/double-alt-arrow-down-line-duotone';

	const dailyChange = 69420;

	let changeDown: boolean = false;
</script>

<div class="col">
	<div class="row main">
		<div id="money-text">
			<h1 class:red={changeDown} class:green={!changeDown}>
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
	$duration: 1s;

	.col {
		display: flex;
		flex-direction: column;
		align-items: center;
		justify-content: center;
		height: 100vh;
	}

	.row {
		display: flex;
		align-items: center;
		justify-content: space-between;
		max-width: 75vw;
		width: 100%;

		background-color: #022842;
		border-radius: 2rem;
		filter: drop-shadow(2px 2px 2px #000000);

		&.main {
			height: 65vh;
			padding-left: 6rem;
			padding-right: 6rem;
		}

		&.header {
			margin-bottom: 5vh;
			height: 10vh;
			padding: 0;
			padding-left: 6rem;

			h1 {
				margin: 0;
				color: white;
				font-weight: 600;
			}
		}
	}

	#doughnut {
		position: relative;
		width: 35rem;
		height: 35rem;
	}

	#money-text {
		h1 {
			color: white;
			font-size: 4rem;

			&.green {
				color: #00ce13;

				:global(svg) {
					animation: slideIn $duration * 1.5;
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
					animation: slideIn $duration * 1.5;
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

			transition: color $duration;
			animation: slideLeft $duration;
		}

		h2 {
			margin: 0;
			color: white;
			font-size: 2.5rem;

			animation: slideRight $duration;
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
	}
</style>
