<script lang="ts">
	import { Chart, type ChartOptions } from 'chart.js/auto';

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

			options: {
				plugins: {
					legend: {
						display: false
					}
				},
				backgroundColor: ['#17ABC4', '#82DAFA', '#00759C', '#9EF1FF', '#4D8CA8', '#0F5E9F']
			} as ChartOptions<'line'>
		});
	}
</script>

<canvas bind:this={canvasElem} />
