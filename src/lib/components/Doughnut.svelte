<script lang="ts">
	import { formatNumber } from '$lib/util.js';
	import Chart, { type ChartOptions } from 'chart.js/auto';
	import ChartDataLabels from 'chartjs-plugin-datalabels';
	import _ from 'lodash';
	import { base } from '$app/paths';
	import { goto } from '$app/navigation';

	export let data: Record<string, number>;

	let labels: string[] = [];
	let values: number[] = [];
	$: {
		const sortedEntries = Object.entries(data).sort((a, b) => a[1] - b[1]);
		labels = sortedEntries.map((elem) => elem[0]);
		values = sortedEntries.map((elem) => elem[1]);
	}

	const otherLabelPercentile = 0.05;

	let totalValue: number;
	$: totalValue = _.sum(values);

	let firstBigIndex: number;
	let otherSectionValue: number;
	$: {
		otherSectionValue = 0;
		firstBigIndex = values.findIndex((v) => {
			if (v / totalValue < otherLabelPercentile) {
				otherSectionValue += v;
				return false;
			}
			return true;
		});
		if (!firstBigIndex || firstBigIndex <= 1) firstBigIndex = -1;
	}

	let canvasElem: HTMLCanvasElement;
	let chart: any;
	$: if (canvasElem) {
		if (chart) chart.destroy();
		chart = new Chart(canvasElem, {
			type: 'doughnut',
			data: {
				labels: labels,
				datasets: [
					{
						label: 'Amount',
						data: values
					}
				]
			},
			plugins: [ChartDataLabels],
			options: {
				plugins: {
					datalabels: {
						color: 'white',
						align: 'end',
						anchor: 'end',
						formatter(value, context) {
							const labels = context.chart.data.labels;
							if (context.dataIndex == 0 && firstBigIndex > 0)
								return `Other\n${Math.round((otherSectionValue / totalValue) * 10000) / 100}%`;
							if (labels)
								return `${labels[context.dataIndex]}\n${
									Math.round((value / totalValue) * 10000) / 100
								}%`;
						},
						font: {
							size: 16
						},
						offset: 5,
						textAlign: 'center',
						display(context) {
							return context.dataIndex >= firstBigIndex || context.dataIndex == 0;
						}
					},
					legend: {
						display: false
					}
				},
				color: 'black',
				borderWidth: 0,
				layout: {
					padding: 100
				},
				cutout: '75%',
				backgroundColor: ['#17ABC4', '#82DAFA', '#00759C', '#9EF1FF', '#4D8CA8', '#0F5E9F'],
				animation: {
					duration: 1000,
					easing: 'easeOutCubic'
				},
				onClick(event, elements, chart) {
					const elem = elements[0];
					goto(`${base}/assets?type=${labels[elem.index]}`);
				}
			} as ChartOptions<'doughnut'>
		});
	}
</script>

<div class="container">
	<div class="overlay">
		<div>
			<h1>${formatNumber(totalValue)}</h1>
			<h2>TOTAL NET WORTH</h2>
		</div>
	</div>
	<canvas bind:this={canvasElem} />
</div>

<style lang="scss">
	canvas:hover {
		position: relative;
		z-index: 10;
	}

	.container {
		aspect-ratio: 1;
	}

	.overlay {
		position: absolute;
		top: 0;
		left: 0;
		right: 0;
		bottom: 0;

		display: flex;
		align-items: center;
		justify-content: center;

		color: white;

		pointer-events: none;

		div {
			display: flex;
			align-items: center;
			justify-content: center;
			flex-direction: column;

			* {
				margin: 0;
			}

			h1 {
				font-size: 2vw;
			}

			h2 {
				font-size: 1vw;
			}
		}

		animation: fadeIn 1s;
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
