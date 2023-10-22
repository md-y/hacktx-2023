// @ts-nocheck

import { sum } from 'lodash';
import { get } from 'svelte/store';
import { user } from './store';

/**
 * @param {Date | number} time
 * @returns {Record<string, number>}
 */
export function getDoughnutData(time = Date.now()) {
	const userData = get(user);

	/**
	 * @type {Record<string, number>}
	 */
	const assetTypes = {};
	for (const asset of userData.assets) {
		if (new Date(asset.starting_date) > time) continue;
		if (!(asset.asset_type in assetTypes)) assetTypes[asset.asset_type] = 0;
		assetTypes[asset.asset_type] += getCurrentAssetValue(asset, time);
	}

	let currentBalance = userData.checking_account_balance + userData.savings_account_balance;
	const futureWithdrawals = sum(
		userData.withdrawls.filter((w) => new Date(w.date) > time).map((w) => w.amount)
	);
	const futureDeposits = sum(
		userData.deposits.filter((d) => new Date(d.date) > time).map((d) => d.amount)
	);

	assetTypes['Monetary Assets'] = currentBalance + futureWithdrawals - futureDeposits;

	// TODO: Liabilities?

	return assetTypes;
}

/**
 * @param {Date | number} time
 * @returns {number}
 */
export function getNetWorth(time = Date.now()) {
	const data = getDoughnutData(time);
	return sum(Object.values(data));
}

/**
 * @param {*} asset
 * @param {Date | number} time
 * @returns
 */
export function getCurrentAssetValue(asset, time = Date.now()) {
	const t = (time - new Date(asset.starting_date)) / 1000 / 60 / 60 / 24 / 365;
	/**
	 * @type {number}
	 */
	const init = asset.initial_value;
	/**
	 * @type {number}
	 */
	const r = asset.r;
	/**
	 * @type {number}
	 */
	const minmax = asset.min_max_value;
	let val = 0;

	switch (asset.function_type) {
		case 'exponential':
			val = init * Math.pow(1 + r, t);
			break;
		case 'linear':
			val = init + t * r;
			break;
		case 'logistic':
			val = (minmax / init - 1) / Math.pow(Math.E, -1 * r * t);
			break;
	}

	return val;
}
