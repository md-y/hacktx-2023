<script>
	// @ts-nocheck

	// Import the functions you need from the SDKs you need
	import {
		signInWithPopup,
		signOut,
		signInWithEmailAndPassword,
		createUserWithEmailAndPassword
	} from 'firebase/auth';
	import { auth, provider } from '../lib/util.js';
	import { user, wirelessMode, authToken } from '../lib/store.js';

	import AES from 'crypto-js/aes';
	import CryptoJS from 'crypto-js';
	import { goto } from '$app/navigation';
	import { get } from 'lodash';
	import { Button, FileUploaderButton, PasswordInput, TextInput } from 'carbon-components-svelte';
	import MdiGoogle from '~icons/mdi/google';
	import { base } from '$app/paths';

	//my code

	let loggedIn = false;
	let uid = undefined;
	let email = '';
	let password = '';
	let encryptedFilePassword = '';
	let encryptedFile = false;
	let signUpPage = false;

	auth.onAuthStateChanged(async (user) => {
		loggedIn = user ? true : false;
		if (loggedIn) {
			uid = user.uid;
			if ($authToken == '') {
				await fetchAuthToken();
			}
			await getData();
			goto('/dashboard');
		} else {
			uid = undefined;
			$authToken = '';
		}
	});

	async function getData() {
		try {
			const at = $authToken;
			let response = await fetch('https://helloworld-feagyby2hq-uc.a.run.app/user', {
				headers: {
					AuthToken: at
				}
			});
			const userData = await response.json();
			$user = userData;
		} catch (error) {
			console.log(error);
		}
	}

	async function previewFile() {
		const content = document.querySelector('.content');
		const [file] = document.querySelector('input[type=file]').files;
		const reader = new FileReader();

		reader.addEventListener(
			'load',
			() => {
				//this updates the userData
				const userData = JSON.parse(
					decryptData(reader.result, encryptedFilePassword).toString(CryptoJS.enc.Utf8)
				);

				$user = userData;
				$wirelessMode = true;
				goto('/dashboard');
			},
			false
		);

		if (file) {
			reader.readAsText(file);
		}
	}

	function encryptData(data, key) {
		return AES.encrypt(data, key);
	}

	function decryptData(data, key) {
		return AES.decrypt(data, key);
	}

	async function fetchAuthToken() {
		if (auth.currentUser) {
			const at = await auth.currentUser.getIdToken(true);
			$authToken = at;
		}
	}

	function userpassLogin() {
		signInWithEmailAndPassword(auth, email, password);
		fetchAuthToken();
	}

	function googleLogin() {
		signInWithPopup(auth, provider);
		fetchAuthToken();
	}

	function logout() {
		signOut(auth);
	}
</script>

<h1>Am I Broke?</h1>
<div id="parent">
	{#if encryptedFile}
		<div class="kid">
			<a
				href={base}
				on:click={() => {
					encryptedFile = false;
					signUpPage = false;
				}}>Return to other sign in options</a
			>
			<br />
			<div class="file-upload">
				<FileUploaderButton labelText="Upload File" />
			</div>
			<br />
			<PasswordInput bind:value={encryptedFilePassword} placeholder="Encrypted File Password" />
			<br />
			<Button on:click={previewFile}>Read data</Button>
		</div>
	{:else if signUpPage}
		<div class="kid">
			<a
				href={base}
				on:click={() => {
					encryptedFile = false;
					signUpPage = false;
				}}>Return to other sign in options</a
			>
			<br />
			<div class="signup-email"><TextInput bind:value={email} placeholder="Email" /></div>
			<br />
			<PasswordInput bind:value={password} placeholder="Password" />
			<br />
			<Button on:click={createUserWithEmailAndPassword(auth, email, password)}>Sign Up</Button>
		</div>
	{:else}
		<div class="kid">
			<TextInput bind:value={email} placeholder="Email" />
			<br />
			<PasswordInput bind:value={password} placeholder="Password" />
			<br />
			<p>Dont have account <a href="./" on:click={() => (signUpPage = true)}>Sign Up</a></p>
			<br />
			<Button on:click={userpassLogin} kind="primary">Sign In</Button>
			<hr />
			<div class="google">
				<Button on:click={googleLogin} icon={MdiGoogle}>Continue With Google</Button>
			</div>
			<br />
			<Button on:click={() => (encryptedFile = true)}>Continue With EncryptedFile</Button>
		</div>
	{/if}
</div>

<style>
	.kid {
		background-color: #022842;
		padding: 4rem;
		border-radius: 2rem;
	}

	p {
		color: white;
	}

	hr {
		margin-top: 1rem;
		margin-bottom: 1rem;
	}

	a {
		font-size: large;
		margin-bottom: 1rem;
		color: #c4c9ff;
	}

	.google {
		margin-bottom: 0.25rem;
	}

	#parent {
		display: flex;
		justify-content: center;
	}
	h1 {
		color: white;
		font-weight: 800;
		text-align: center;
		padding-top: 5%;
		padding-bottom: 5%;
		font-size: 6rem;
	}

	.file-upload,
	.signup-email {
		margin-top: 1rem;
		margin-bottom: 0.25rem;
	}
</style>
