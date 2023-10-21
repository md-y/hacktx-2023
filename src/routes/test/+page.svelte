<script>
	// Import the functions you need from the SDKs you need
	import { initializeApp } from 'firebase/app';
	import { getAuth, signInWithPopup, signOut } from 'firebase/auth';
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
	const app = initializeApp(firebaseConfig);
	const auth = getAuth(app);
	const provider = new GoogleAuthProvider();

	//mycode
	let loggedIn = false;
	let authToken = undefined;
	auth.onAuthStateChanged((user) => {
		loggedIn = user ? true : false;
		if (loggedIn) {
			if (authToken == undefined) {
				fetchAuthToken();
			}
		} else {
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
		console.log('logging you in');
		console.log(auth);
	}

	function logout() {
		signOut(auth);
		console.log('logging you out');
	}

	async function testWithBackend() {
		try {
			let response = await fetch('http://127.0.0.1:2000/user', {
				headers: {
					AuthToken: authToken
				}
			});
			response = await response.json();
			console.log(response);
		} catch (error) {
			console.log(error);
		}
	}
</script>

<button on:click={login}>Login</button>
<button on:click={logout}>Logout</button>
<p>Logged in status: {loggedIn}</p>
<button on:click={testWithBackend}>Test interaction with backend</button>
<p>{authToken}</p>
