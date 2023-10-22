<script lang="ts">
	import { Chart, type ChartOptions } from 'chart.js/auto';
	import { merge } from 'lodash';

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

	export let options: ChartOptions<'line'> = {};

	let canvasElem: HTMLCanvasElement;
	$: if (canvasElem) {
		new Chart(canvasElem, {
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
			options: merge(
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
								color: 'white'
							}
						},
						x: {
							grid: {
								color: 'transparent'
							},
							ticks: {
								color: 'white'
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
