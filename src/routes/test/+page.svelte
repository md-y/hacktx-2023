<script>
	// @ts-nocheck

	// Import the functions you need from the SDKs you need
	import { initializeApp } from 'firebase/app';
	import { getAuth, signInWithPopup, signOut } from 'firebase/auth';
	import { GoogleAuthProvider } from 'firebase/auth';
	import AES from 'crypto-js/aes';
	import CryptoJS from 'crypto-js';

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
	const app = initializeApp(firebaseConfig);
	const auth = getAuth(app);
	const provider = new GoogleAuthProvider();

	//mycode
	let loggedIn = false;
	let authToken = undefined;
	let userData = undefined;
	let uid = undefined;
	let decryptPassword = undefined;

	auth.onAuthStateChanged((user) => {
		loggedIn = user ? true : false;
		if (loggedIn) {
			uid = user.uid;
			if (authToken == undefined) {
				fetchAuthToken();
			}
		} else {
			uid = undefined;
			authToken = undefined;
		}
	});

	async function fetchAuthToken() {
		if (auth.currentUser) {
			authToken = await auth.currentUser.getIdToken(true);
			authToken = authToken;
		}
	}

	function login() {
		signInWithPopup(auth, provider);
		fetchAuthToken();
		loginToBackend();
		console.log('logging you in');
		console.log(auth);
	}

	function logout() {
		signOut(auth);
		console.log('logging you out');
	}

	async function getData() {
		try {
			let response = await fetch('https://helloworld-feagyby2hq-uc.a.run.app/user', {
				headers: {
					AuthToken: authToken
				}
			});
			userData = await response.json();
		} catch (error) {
			console.log(error);
		}
	}

	async function postData() {
		try {
			let response = await fetch('https://helloworld-feagyby2hq-uc.a.run.app/user', {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json',
					AuthToken: authToken
				},
				body: JSON.stringify(userData)
			});
		} catch (error) {
			console.log(error);
		}
	}

	async function pushData() {
		try {
			let response = await fetch('https://helloworld-feagyby2hq-uc.a.run.app/user', {
				method: 'PUT',
				headers: {
					'Content-Type': 'application/json',
					AuthToken: authToken
				},
				body: JSON.stringify(userData)
			});
		} catch (error) {
			console.log(error);
		}
	}

	function downloadData() {
		//code to encrypt file
		let encryptedData = encryptData(JSON.stringify(userData), decryptPassword).toString();

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

	async function previewFile() {
		const content = document.querySelector('.content');
		const [file] = document.querySelector('input[type=file]').files;
		const reader = new FileReader();

		reader.addEventListener(
			'load',
			() => {
				//this updates the userData
				userData = JSON.parse(
					decryptData(reader.result, decryptPassword).toString(CryptoJS.enc.Utf8)
				);
			},
			false
		);

		if (file) {
			reader.readAsText(file);
		}
	}

	function stringToFloat(s) {
		return parseFloat(s.replace(',', ''));
	}

	function calculateLinearR(initial_value, buy_date, current_value, current_date) {
		return (current_value - initial_value) / (current_date - buy_date);
	}

	function calculateExponentialR(initial_value, buy_date, current_value, current_date) {
		if (current_date === buy_date) {
			return 0;
		}
		return (current_value / initial_value) ** (1 / (current_date - buy_date)) - 1;
	}

	// Newton-Raphson Method
	function newtonRaphson(func, derivative, initialGuess, tolerance = 1e-6, maxIterations = 1000) {
		let x0 = initialGuess;
		let x1;

		for (let i = 0; i < maxIterations; i++) {
			x1 = x0 - func(x0) / derivative(x0);

			if (Math.abs(x1 - x0) <= tolerance) {
				return x1;
			}

			x0 = x1;
		}
		throw new Error('Newton-Raphson method did not converge');
	}

	function calculateLogisticR(initial_value, buy_date, current_value, current_date) {
		const L = 2 * initial_value;
		const time_difference = current_date - buy_date;
		const c = L / initial_value - 1;

		const logisticFunction = (R) => {
			return current_value - L / (1 + c * Math.exp(-R * time_difference));
		};

		const logisticFunctionDerivative = (R) => {
			return (
				(L * c * time_difference * Math.exp(-R * time_difference)) /
				(1 + c * Math.exp(-R * time_difference)) ** 2
			);
		};

		try {
			const R = newtonRaphson(logisticFunction, logisticFunctionDerivative, 0.05);
			return R;
		} catch (e) {
			console.error(e.message);
			return null;
		}
	}

	async function suggestRValue(asset, function_type) {
		const API_ENDPOINT = 'https://api.openai.com/v1/engines/davinci/completions';
		const API_KEY = 'YOUR_OPENAI_API_KEY';

		const messages = [
			{
				role: 'system',
				content: `Please provide a ${function_type} growth/decay rate, R, for modeling ${asset} appreciation/depreciation. Make sure it is realistic and varies with different assets and function types. Make the R value negative if you think the asset depreciates and positive if you think the asset appreciates. Always return an R value.`
			}
		];

		const response = await fetch(API_ENDPOINT, {
			method: 'POST',
			headers: {
				Authorization: `Bearer ${API_KEY}`,
				'Content-Type': 'application/json'
			},
			body: JSON.stringify({
				model: 'gpt-3.5-turbo',
				messages: messages,
				max_tokens: 2000
			})
		});

		const data = await response.json();

		const suggested_R_value = data.choices[0].message.content.trim();
		const numberMatches = suggested_R_value.match(/[-+]?\d*\.\d+|\d+/g);

		if (!numberMatches) {
			throw new Error('Failed to extract a valid number from GPT response.');
		}

		return parseFloat(numberMatches[0]);
	}

	function encryptData(data, key) {
		return AES.encrypt(data, key);
	}

	function decryptData(data, key) {
		return AES.decrypt(data, key);
	}
</script>

<button on:click={login}>Login</button>
<button on:click={logout}>Logout</button>
<p>Logged in status: {loggedIn}</p>
<button on:click={getData}>Get data</button>
<button on:click={postData}>Post data</button>
<button on:click={pushData}>Put data</button>
<button on:click={downloadData}>Download data</button>
<input type="file" on:change={previewFile} />
<label for="decryptPassword"> password for file</label>
<input id="decryptPassword" type="password" bind:value={decryptPassword} />
<p class="content" />
<p>{JSON.stringify(userData)}</p>
