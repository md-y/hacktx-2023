<script>
	// @ts-nocheck

		// Import the functions you need from the SDKs you need
	import { initializeApp } from "firebase/app";
	import { getAuth, signInWithPopup, signOut} from "firebase/auth";
	import { GoogleAuthProvider } from "firebase/auth";

	// TODO: Add SDKs for Firebase products that you want to use
	// https://firebase.google.com/docs/web/setup#available-libraries

	// Your web app's Firebase configuration
	// For Firebase JS SDK v7.20.0 and later, measurementId is optional
	const firebaseConfig = {
	apiKey: "AIzaSyBWqnf7hw8AgFif5swkvWJx3CoERDJCgdo",
	authDomain: "hacktx2023.firebaseapp.com",
	projectId: "hacktx2023",
	storageBucket: "hacktx2023.appspot.com",
	messagingSenderId: "908408891172",
	appId: "1:908408891172:web:467345a36027012a1e75b1",
	measurementId: "G-SS4CK9CSEH"
	};



	// Initialize Firebase
	const app = initializeApp(firebaseConfig);
	const auth = getAuth(app);
	const provider = new GoogleAuthProvider();

	//mycode
	let loggedIn = false;
	let authToken = undefined;
	let userData = undefined;
	auth.onAuthStateChanged(user => {
		loggedIn = user ? true : false;
		if(loggedIn){
			if(authToken == undefined){
				fetchAuthToken();
			}
		}else{
			authToken = undefined;
		}
	})

	async function fetchAuthToken(){
		if (auth.currentUser) {
			authToken = await auth.currentUser.getIdToken(true);
			authToken = authToken;
		}
	}

	function login(){
		signInWithPopup(auth, provider);
		fetchAuthToken();
		console.log("logging you in");
		console.log(auth)
	}

	function logout(){
		signOut(auth);
		console.log("logging you out");
	}

	async function testWithBackend(){
		try{
			let response = await fetch("http://127.0.0.1:2000/user", {
				headers: {
					"AuthToken": authToken
				}
			});
			userData = await response.json();
		}
		catch(error){
			console.log(error)
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
      		return current_value - (L / (1 + c * Math.exp(-R * time_difference)));
  		};

  		const logisticFunctionDerivative = (R) => {
      		return L * c * time_difference * Math.exp(-R * time_difference) / 
             ((1 + c * Math.exp(-R * time_difference)) ** 2);
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
    const API_ENDPOINT = "https://api.openai.com/v1/engines/davinci/completions"; 
    const API_KEY = "YOUR_OPENAI_API_KEY";

    const messages = [{
        "role": "system",
        "content": `Please provide a ${function_type} growth/decay rate, R, for modeling ${asset} appreciation/depreciation. Make sure it is realistic and varies with different assets and function types. Make the R value negative if you think the asset depreciates and positive if you think the asset appreciates. Always return an R value.`
    }];

    const response = await fetch(API_ENDPOINT, {
        method: 'POST',
        headers: {
            'Authorization': `Bearer ${API_KEY}`,
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            model: "gpt-3.5-turbo",
            messages: messages,
            max_tokens: 2000,
        })
    });

    const data = await response.json();

    const suggested_R_value = data.choices[0].message.content.trim();
    const numberMatches = suggested_R_value.match(/[-+]?\d*\.\d+|\d+/g);

    if (!numberMatches) {
        throw new Error("Failed to extract a valid number from GPT response.");
    }

    return parseFloat(numberMatches[0]);
	}
</script>

<button on:click={login}>Login</button>
<button on:click={logout}>Logout</button>
<p>Logged in status: {loggedIn}</p>
<button on:click={testWithBackend}>Test interaction with backend</button>
<p>{JSON.stringify(userData)}</p>