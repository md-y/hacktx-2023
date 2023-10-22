<script lang="ts">
	import { getCurrentAssetValue } from '$lib/assets';
	import { user } from '$lib/store';
	import { formatNumber } from '$lib/util';
	import { Chart } from 'chart.js/auto';
	import ChartDataLabels from 'chartjs-plugin-datalabels';
	import _ from 'lodash';

	const assetData = $user;
	const labels: string[] = [];
	const values: number[] = [];

	const assets = [];
	for (const asset of assetData.assets) {
		assets.push({ ...asset, current_amount: getCurrentAssetValue(asset) });
	}

	const groupedAssets = _.sortBy(Object.entries(_.groupBy(assets, 'asset_type')), ([, arr]) =>
		_.sum(arr.map((a) => a.current_amount))
	).reverse();
	for (const [i, arr] of groupedAssets) {
		labels.push(i);
		const sortedArr = _.sortBy(arr, (a) => a.current_amount).reverse();
		const assetValues = sortedArr.map((a) => a.current_amount);
		const assetLabels = sortedArr.map((a) => `> ${a.asset_name}`);
		values.push(_.sum(assetValues));
		labels.push(...assetLabels);
		values.push(...assetValues);
	}

	const colors = ['#00759C', '#9EF1FF', '#82DAFA', '#4D8CA8', '#0F5E9F', '#17ABC4'];

	let canvasElem: HTMLCanvasElement;
	$: if (canvasElem) {
		new Chart(canvasElem, {
			type: 'bar',
			data: {
				labels: labels,
				datasets: [
					{
						label: 'Amount ($)',
						data: values
					}
				]
			},
			plugins: [ChartDataLabels],
			options: {
				indexAxis: 'y',
				maintainAspectRatio: false,
				plugins: {
					legend: {
						display: false
					},
					datalabels: {
						align: 'end',
						anchor: 'end',
						color: 'white',
						formatter(value) {
							return formatNumber(value);
						}
					}
				},
				elements: {
					bar: {
						backgroundColor(ctx, options) {
							let index = 0;
							for (let i = ctx.dataIndex; i >= 0; i--) {
								if (!labels[i].startsWith('> ')) index++;
							}
							return colors[index % colors.length];
						},
						borderColor: 'rgba(255, 255, 255, 0.8)',
						borderWidth(ctx) {
							if (!labels[ctx.dataIndex].startsWith('> ')) return 5;
							return 0;
						},
						borderRadius: 20
					}
				},
				scales: {
					y: {
						ticks: {
							color: 'white',
							autoSkip: false,
							callback(tickValue, index, ticks) {
								const str = labels[index];
								if (str.startsWith('> ')) {
									return str.slice(2);
								}
								return str;
							},
							font(ctx, options) {
								const str = labels[ctx.index];
								return str.startsWith('>')
									? {
											size: 16,
											weight: 'normal',
											style: 'italic'
									  }
									: {
											size: 24,
											weight: 'bold'
									  };
							}
						}
					},
					x: {
						position: 'top',
						ticks: {
							color: 'white',
							font: {
								size: 20
							},
							callback(tickValue, index, ticks) {
								return formatNumber(tickValue as number);
							}
						}
					}
				}
			}
		});
	}
</script>

<canvas bind:this={canvasElem} />
