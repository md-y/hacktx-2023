import { writable } from 'svelte/store';

export const wirelessMode = writable(false);
export const authToken = writable("");

export const user = writable({
	assets: [
		{
			asset_type: 'Default Type',
			asset_name: 'Default Asset',
			function_type: 'exponential',
			initial_value: 1000,
			min_max_value: 0,
			r: -0.2,
			starting_date: '3/23/2009'
		},
	],
	bills: [
		{
			payment_amount: 0,
			payment_date: '10/21/2023'
		}
	],
	checking_account_balance: 0,
	checking_account_reward: 0,
	credit_card_balance: 0,
	credit_card_rewards: 0,
	deposits: [
		{
			account: 'checkings',
			amount: 0,
			date: '08/21/2021'
		}
	],
	monthly_bills: [
		{
			amount: 0
		}
	],
	savings_account_balance: 0,
	savings_account_rewards: 0,
	withdrawls: [
		{
			account: 'checkings',
			amount: 0,
			date: '10/21/2022'
		}
	]
});
