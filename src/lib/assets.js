// @ts-nocheck
const DB = {
	assets: [
		{
			asset_type: 'Car',
			asset_name: '2010 Ford Mustang',
			function_type: 'exponential',
			initial_value: '28845',
			min_max_value: 0,
			r: -0.2,
			starting_date: '3/23/2009'
		},

		{
			asset_type: 'Car',
			asset_name: '2024 Toyota Camry',
			function_type: 'exponential',
			initial_value: '26420',
			min_max_value: 0,
			r: -0.2,
			starting_date: '09/15/2023'
		},

		{
			asset_type: 'Property',
			asset_name: 'House',
			function_type: 'exponential',
			initial_value: '350000',
			min_max_value: 0,
			r: 0.06,
			starting_date: '04/06/2011'
		},

		{
			asset_type: 'Technology',
			asset_name: 'Desktop PC',
			function_type: 'exponential',
			initial_value: '950',
			min_max_value: 0,
			r: -0.1,
			starting_date: '05/01/2019'
		},

		{
			asset_type: 'Technology',
			asset_name: 'iPhone 15 Pro Max',
			function_type: 'exponential',
			initial_value: '1200',
			min_max_value: -0.1,
			r: 0.5,
			starting_date: '10/06/2023'
		},

		{
			asset_type: 'Asset Type',
			asset_name: 'Asset Name',
			function_type: 'exponential',
			initial_value: '0',
			min_max_value: 0,
			r: 0.5,
			starting_date: '10/21/2023'
		},
		{
			asset_type: 'Asset Type',
			asset_name: 'Asset Name',
			function_type: 'exponential',
			initial_value: '0',
			min_max_value: 0,
			r: 0.5,
			starting_date: '10/21/2023'
		},
		{
			asset_type: 'Asset Type',
			asset_name: 'Asset Name',
			function_type: 'exponential',
			initial_value: '0',
			min_max_value: 0,
			r: 0.5,
			starting_date: '10/21/2023'
		},
		{
			asset_type: 'Asset Type',
			asset_name: 'Asset Name',
			function_type: 'exponential',
			initial_value: '0',
			min_max_value: 0,
			r: 0.5,
			starting_date: '10/21/2023'
		},
		{
			asset_type: 'Asset Type',
			asset_name: 'Asset Name',
			function_type: 'exponential',
			initial_value: '0',
			min_max_value: 0,
			r: 0.5,
			starting_date: '10/21/2023'
		},
		{
			asset_type: 'Asset Type',
			asset_name: 'Asset Name',
			function_type: 'exponential',
			initial_value: '0',
			min_max_value: 0,
			r: 0.5,
			starting_date: '10/21/2023'
		},
		{
			asset_type: 'Asset Type',
			asset_name: 'Asset Name',
			function_type: 'exponential',
			initial_value: '0',
			min_max_value: 0,
			r: 0.5,
			starting_date: '10/21/2023'
		},
		{
			asset_type: 'Asset Type',
			asset_name: 'Asset Name',
			function_type: 'exponential',
			initial_value: '0',
			min_max_value: 0,
			r: 0.5,
			starting_date: '10/21/2023'
		},
		{
			asset_type: 'Asset Type',
			asset_name: 'Asset Name',
			function_type: 'exponential',
			initial_value: '0',
			min_max_value: 0,
			r: 0.5,
			starting_date: '10/21/2023'
		},
		{
			asset_type: 'Asset Type',
			asset_name: 'Asset Name',
			function_type: 'exponential',
			initial_value: '0',
			min_max_value: 0,
			r: 0.5,
			starting_date: '10/21/2023'
		},
		{
			asset_type: 'Asset Type',
			asset_name: 'Asset Name',
			function_type: 'exponential',
			initial_value: '0',
			min_max_value: 0,
			r: 0.5,
			starting_date: '10/21/2023'
		},
		{
			asset_type: 'Asset Type',
			asset_name: 'Asset Name',
			function_type: 'exponential',
			initial_value: '0',
			min_max_value: 0,
			r: 0.5,
			starting_date: '10/21/2023'
		},
		{
			asset_type: 'Asset Type',
			asset_name: 'Asset Name',
			function_type: 'exponential',
			initial_value: '0',
			min_max_value: 0,
			r: 0.5,
			starting_date: '10/21/2023'
		},
		{
			asset_type: 'Asset Type',
			asset_name: 'Asset Name',
			function_type: 'exponential',
			initial_value: '0',
			min_max_value: 0,
			r: 0.5,
			starting_date: '10/21/2023'
		},
		{
			asset_type: 'Asset Type',
			asset_name: 'Asset Name',
			function_type: 'exponential',
			initial_value: '0',
			min_max_value: 0,
			r: 0.5,
			starting_date: '10/21/2023'
		},
		{
			asset_type: 'Asset Type',
			asset_name: 'Asset Name',
			function_type: 'exponential',
			initial_value: '0',
			min_max_value: 0,
			r: 0.5,
			starting_date: '10/21/2023'
		}
	],
	bills: [
		{
			payment_amount: 0,
			payment_date: '10/21/2023'
		}
	],
	checking_account_balance: 10000,
	checking_account_reward: 0,
	credit_card_balance: 0,
	credit_card_rewards: 1000,
	deposits: [
		{
			account: 'checkings',
			amount: 0,
			date: '10/21/2023'
		}
	],
	monthly_bills: [
		{
			amount: 0
		}
	],
	savings_account_balance: 0,
	savings_account_rewards: 0,
	uid: '',
	withdrawls: [
		{
			account: 'checkings',
			amount: 0,
			date: '10/21/2023'
		}
	]
};

/**
 * @returns {Record<string, number>}
 */
export function getDoughnutData() {
	const assetTypes = {};
	for (const asset of DB.assets) {
		if (!(asset.asset_type in assetTypes)) assetTypes[asset.asset_type] = 0;
		assetTypes[asset.asset_type] += getCurrentAssetValue(asset);
	}

	let monetaryAssets = 0;
	monetaryAssets += DB.checking_account_balance;
	monetaryAssets += DB.savings_account_balance;
	monetaryAssets += DB.credit_card_rewards;
	assetTypes['Monetary Assets'] = monetaryAssets;

	// TODO: Liabilities?

	return assetTypes;
}

export function getCurrentAssetValue(asset) {
	const t = (Date.now() - new Date(asset.starting_date)) / 1000 / 60 / 60 / 24 / 365;
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
