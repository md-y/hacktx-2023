<script lang="ts">
	import { numberWithCommas } from '$lib/util';
	import Chart, { type ChartOptions } from 'chart.js/auto';
	import ChartDataLabels from 'chartjs-plugin-datalabels';

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
	$: totalValue = values.reduce((d, v) => v + d, 0);

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
	$: if (canvasElem) {
		new Chart(canvasElem, {
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
						color: 'black',
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
				}
			} as ChartOptions<'doughnut'>
		});
	}
</script>

<div class="container">
	<div class="overlay">
		<h1>${numberWithCommas(totalValue.toString())}</h1>
	</div>
	<canvas bind:this={canvasElem} />
</div>

<style lang="scss">
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
	}
</style>
