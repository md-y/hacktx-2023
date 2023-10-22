<script lang="ts">
	import { formatNumber } from '$lib/util';
	import { Chart, type ChartOptions } from 'chart.js/auto';
	import _ from 'lodash';

	export let yValues: number[] | ((val: number) => number);
	// If not labels: start value, end value, step
	export let xValues: number[] | [number, number, number];
	$: {
		if (!Array.isArray(yValues)) {
			const newYValues = [];
			if (xValues.length === 3) {
				const newXValues = [];
				for (let i = xValues[0]; i < xValues[1]; i += xValues[2]) {
					newYValues.push(yValues(i));
					newXValues.push(i);
				}
				xValues = newXValues;
			} else {
				for (let i of xValues) {
					newYValues.push(yValues(i));
				}
			}
			yValues = newYValues;
		}
	}

	export let startDate: Date | undefined = undefined;

	export let options: ChartOptions<'line'> = {};

	let canvasElem: HTMLCanvasElement;
	let chart: any;
	$: if (canvasElem) {
		if (chart) chart.destroy();
		chart = new Chart(canvasElem, {
			type: 'line',
			data: {
				labels: xValues,
				datasets: [
					{
						label: 'Amount',
						data: yValues
					}
				]
			},
			options: _.merge(
				{
					plugins: {
						legend: {
							display: false
						}
					},
					maintainAspectRatio: false,
					elements: {
						line: {
							borderColor: 'white'
						},
						point: {
							backgroundColor: 'transparent'
						}
					},
					scales: {
						y: {
							grid: {
								color: 'transparent'
							},
							ticks: {
								color: 'white',
								callback(tickValue) {
									return `$${formatNumber(tickValue as number)}`;
								}
							}
						},
						x: {
							grid: {
								color: 'transparent'
							},
							ticks: {
								color: 'white',
								callback(tickValue) {
									if (!startDate || typeof tickValue === 'string') return tickValue;
									const date = new Date(startDate.getTime() + tickValue * 24 * 60 * 60 * 1000);
									return `${date.getMonth() + 1}/${date.getDate()}/${date.getFullYear() % 100}`;
								}
							}
						}
					}
				} as ChartOptions<'line'>,
				options
			)
		});
	}
</script>

<canvas bind:this={canvasElem} />
