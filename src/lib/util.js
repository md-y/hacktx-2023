/**
 * @param {number} x
 * @returns {string}
 */
export function formatNumber(x) {
	let suffix = '';
	if (x > 1000000000) {
		x /= 1000000000;
		suffix += 'b';
	} else if (x > 1000000) {
		x /= 1000000;
		suffix += 'm';
	} else if (x > 1000) {
		x /= 1000;
		suffix += 'k';
	}
	x = Math.round(x * 10) / 10;
	return `${x.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ',')}${suffix}`;
}
