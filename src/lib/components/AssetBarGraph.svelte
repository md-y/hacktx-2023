<script lang="ts">
	import { getCurrentAssetValue } from '$lib/assets';
	import { user, authToken } from '$lib/store';
	import { formatNumber } from '$lib/util';
	import { Chart } from 'chart.js/auto';
	import ChartDataLabels from 'chartjs-plugin-datalabels';
	import _ from 'lodash';

	export let focusType: string | undefined = undefined;

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
		if (focusType && i != focusType) continue;
		const sortedArr = _.sortBy(arr, (a) => a.current_amount).reverse();
		const assetValues = sortedArr.map((a) => a.current_amount);
		const assetLabels = sortedArr.map((a) => `> ${a.asset_name}`);
		if (!focusType) {
			labels.push(i);
			values.push(_.sum(assetValues));
		}
		labels.push(...assetLabels);
		values.push(...assetValues);
	}

	const colors = ['#00759C', '#9EF1FF', '#82DAFA', '#4D8CA8', '#0F5E9F', '#17ABC4'];

	// async function deleteAsset(name: string) {
	// 	let userData = $user;
	// 	let assetsarray = userData['assets'];
	// 	console.log(assetsarray.length);
	// 	for(let i = 0; i < assetsarray.length; i++){
	// 		if(assetsarray[i]['asset_name'] == name){
	// 			assetsarray.splice(i, 1);
	// 			i--;
	// 		}
	// 	}
	// 	$user = userData;
	// 	await pushData();
	// }

	// async function pushData() {
	// 	try {
	// 		let userData = $user;
	// 		let at = $authToken;
	// 		let response = await fetch('https://helloworld-feagyby2hq-uc.a.run.app/user', {
	// 			method: 'PUT',
	// 			headers: {
	// 				'Content-Type': 'application/json',
	// 				AuthToken: at
	// 			},
	// 			body: JSON.stringify(userData)
	// 		});
	// 	} catch (error) {
	// 		console.log(error);
	// 	}
	// }

	let canvasElem: HTMLCanvasElement;
	let chart: any;
	$: if (canvasElem) {
		if (chart) chart.destroy();
		chart = new Chart(canvasElem, {
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
						borderRadius: 20,
						hoverBackgroundColor(ctx, options) {
							let index = 0;
							for (let i = ctx.dataIndex; i >= 0; i--) {
								if (!labels[i].startsWith('> ')) index++;
							}
							const normalColor = colors[index % colors.length];
							if (!labels[ctx.dataIndex].startsWith('> ')) return normalColor;
							else return '#ff3131';
						}
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
				},
				onClick(event, elements, chart) {
					if (elements.length > 0) {
						const label = labels[elements[0].index];
						if (!label.startsWith('> ')) return;
						deleteAsset(label.slice(2));
					}
				}
			}
		});
	}
</script>

<canvas bind:this={canvasElem} />
