// @ts-nocheck

import _ from 'lodash';

/**
 * @param {*} userData
 * @param {Date | number} time
 * @returns {Record<string, number>}
 */
export function getDoughnutData(userData, time = Date.now()) {
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
	const futureWithdrawals = _.sum(
		userData.withdrawls.filter((w) => new Date(w.date) > time).map((w) => w.amount)
	);
	const futureDeposits = _.sum(
		userData.deposits.filter((d) => new Date(d.date) > time).map((d) => d.amount)
	);

	currentBalance += futureWithdrawals - futureDeposits;

	const futureLiabilities = _.sum(
		userData.bills.filter((b) => new Date(b.payment_date) > time).map((b) => b.payment_amount)
	);

	currentBalance += futureLiabilities;

	assetTypes['Monetary Assets'] = currentBalance;

	return assetTypes;
}

/**
 * @param {*} userData
 * @param {Date | number} time
 * @returns {number}
 */
export function getNetWorth(userData, time = Date.now()) {
	const data = getDoughnutData(userData, time);
	return _.sum(Object.values(data));
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

	switch (asset.function_type.toLowerCase()) {
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
