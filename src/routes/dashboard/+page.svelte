<script>
	// @ts-nocheck

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
	import AddLiabilityIcon from '~icons/material-symbols/money-off-rounded';
	import AddAssetIcon from '~icons/material-symbols/attach-money';
	import { base } from '$app/paths';
	import NewLiabilityModal from '$components/NewLiabilityModal.svelte';
	import { user } from '$lib/store';
	import { goto } from '$app/navigation';
	import { signOut } from 'firebase/auth';
	import { auth } from '../../lib/util.js';
	import LogoutIcon from '~icons/material-symbols/logout';
	import DownloadIcon from '~icons/material-symbols/download';
	import AES from 'crypto-js/aes';
	import CryptoJS from 'crypto-js';

	let todayAssetData;
	let dailyChange;
	let monthlyChange;
	$: {
		todayAssetData = getDoughnutData($user);
		let todayNetWorth = _.sum(Object.values(todayAssetData));
		let yesterdayAssetData = getNetWorth($user, Date.now() - 24 * 60 * 60 * 1000);
		let lastMonthAssetData = getNetWorth($user, Date.now() - 24 * 60 * 60 * 1000 * 30);
		dailyChange = todayNetWorth - yesterdayAssetData;
		monthlyChange = todayNetWorth - lastMonthAssetData;
	}

	const DAY = 24 * 60 * 60 * 1000;

	let openAssetModal = false;
	let openLiabilityModal = false;

	function logout() {
		signOut(auth);
		goto('/');
	}

	function getDataEncryptionPass(){
		let pass = prompt("Please enter your password to encrypt you data:", "");
		if(pass != null && pass != "")
			downloadData(pass)
	}

	function downloadData(pass) {
		//code to encrypt file
		const userData = $user;
		let encryptedData = encryptData(JSON.stringify(userData), pass).toString();

		//code to download file
		var element = document.createElement('a');
		element.setAttribute(
			'href',
			'data:text/plain;charset=utf-8,' + encodeURIComponent(encryptedData)
		);
		element.setAttribute('download', 'my_secure_financial_data.txt');

		element.style.display = 'none';
		document.body.appendChild(element);

		element.click();

		document.body.removeChild(element);
	}

	function encryptData(data, key) {
		return AES.encrypt(data, key);
	}
</script>

<NewAssetModal bind:open={openAssetModal} />
<NewLiabilityModal bind:open={openLiabilityModal} />

<div class="main-card">
	<div class="row">
		<div class="icons">
			<h1>Am I Broke?</h1>
			<a on:click={() => (openAssetModal = true)}>
				<TooltipIcon icon={AddAssetIcon} tooltipText={'Add new asset'} />
			</a>
			<a on:click={() => (openLiabilityModal = true)}>
				<TooltipIcon icon={AddLiabilityIcon} tooltipText={'Add new liability'} />
			</a>
			<a href="{base}/assets">
				<TooltipIcon icon={BrowseAssetsIcon} tooltipText={'Browse all assets'} />
			</a>
			<a on:click={() => logout()}>
				<TooltipIcon icon={LogoutIcon} tooltipText={'Logout'} />
			</a>
			<a on:click={() => getDataEncryptionPass()}>
				<TooltipIcon icon={DownloadIcon} tooltipText={'Download data'} />
			</a>
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
			{#key todayAssetData}
				<Graph
					xValues={[-365, 0, 1]}
					yValues={(v) => getNetWorth($user, Date.now() + v * DAY)}
					startDate={new Date(Date.now() - 365 * DAY)}
				/>
			{/key}
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

		z-index: 100;

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
