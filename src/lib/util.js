/**
 * @param {number} x
 * @returns {string}
 */

import { initializeApp } from 'firebase/app';
import { getAuth, signInWithPopup, signOut , signInWithEmailAndPassword} from 'firebase/auth';
import { GoogleAuthProvider } from 'firebase/auth';

// TODO: Add SDKs for Firebase products that you want to use
// https://firebase.google.com/docs/web/setup#available-libraries

// Your web app's Firebase configuration
// For Firebase JS SDK v7.20.0 and later, measurementId is optional
const firebaseConfig = {
	apiKey: 'AIzaSyBWqnf7hw8AgFif5swkvWJx3CoERDJCgdo',
	authDomain: 'hacktx2023.firebaseapp.com',
	projectId: 'hacktx2023',
	storageBucket: 'hacktx2023.appspot.com',
	messagingSenderId: '908408891172',
	appId: '1:908408891172:web:467345a36027012a1e75b1',
	measurementId: 'G-SS4CK9CSEH'
};

// Initialize Firebase
export const app = initializeApp(firebaseConfig);
export const auth = getAuth(app);
export const provider = new GoogleAuthProvider();

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
