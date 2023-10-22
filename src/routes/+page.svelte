<script>
    // @ts-nocheck

    // Import the functions you need from the SDKs you need
	import {signInWithPopup, signOut , signInWithEmailAndPassword, createUserWithEmailAndPassword} from 'firebase/auth';
    import {auth, provider} from '../lib/util.js';
    import {user, wirelessMode, authToken} from '../lib/store.js';

	import AES from 'crypto-js/aes';
	import CryptoJS from 'crypto-js';
	import { goto } from '$app/navigation';
	import { get } from 'lodash';

    //my code

    let loggedIn = false;
	let uid = undefined;
    let email = "";
    let password = "";
    let encryptedFilePassword = "";
    let encryptedFile = false;
    let signUpPage = false;

    auth.onAuthStateChanged(async (user) => {
		loggedIn = user ? true : false;
		if (loggedIn) {
			uid = user.uid;
			if ($authToken == "") {
				await fetchAuthToken();
			}
            await getData();
            goto('/dashboard');
		} else {
			uid = undefined;
			$authToken = "";
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
            $user =  userData;
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
                goto("/dashboard")
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

    function userpassLogin(){
        signInWithEmailAndPassword(auth, email, password)
        fetchAuthToken();
    }

    function googleLogin(){
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
            <a href="./" on:click={() => {encryptedFile = false; signUpPage = false}}>return to other sign in options</a>
            <br>
            <input type="file"/>
            <br>
            <label>Password:</label><br>
            <input bind:value={encryptedFilePassword} type="password"/>
            <br>
            <button on:click={previewFile}>Read data</button>
        </div>
    {:else if signUpPage}
    <div class="kid">
        <a href="./" on:click={() => {encryptedFile = false; signUpPage = false}}>return to other sign in options</a>
        <br>
        <label for="emailInput">Email</label>
        <input bind:value={email} id="emailInput"/>
        <br>
        <label for="passwordInput">Password</label>
        <input bind:value={password} type="password" id="passwordInput"/>
        <br>
        <button on:click={createUserWithEmailAndPassword(auth, email, password)}>Sign Up</button>
    </div>
    {:else}
        <div class="kid">
            <label for="emailInput">Email</label>
            <input bind:value={email} id="emailInput"/>
            <br>
            <label for="passwordInput">Password</label>
            <input bind:value={password} type="password" id="passwordInput"/>
            <br>
            <p>Dont have account <a href="./" on:click={()=> signUpPage = true}>Sign Up</a></p> 
            <br>
            <button on:click={userpassLogin}>Sign In</button>
            <p>---------------or---------------</p>
            <button on:click={googleLogin}>Continue With Google</button>
            <br>
            <button on:click={()=> encryptedFile = true}>Continue With EncryptedFile</button>
        </div>
    {/if}

</div>

<style>
    .kid{
        display: flex;
        justify-content: center;
        flex-direction: column;
        align-items: center;
        background-color: white;
        min-width: 25%;
        width: 500px;
        height: 500px;
        max-width: 80%;
        min-height: 50%;
        max-height: 80%;
        border-radius: 10%;
    }
    #parent{
        display: flex;
        justify-content: center;
    }
    h1{
        color: white;
        font-weight: 800;
        text-align: center;
        padding-top: 5%;
        padding-bottom: 5%;
    }
</style>