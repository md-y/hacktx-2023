<script>
    import { Modal, Form, TextInput, NumberInput, Dropdown, Button } from 'carbon-components-svelte';
    import { user } from '../store.js'
    export let open = false;

    let assetType = "";
    let assetName = "";
    let currentValue = 0;
    let growthRateR = 0;
    let initialValue = 0;
    const nowDate = new Date();
    let buyDate = nowDate.getMonth() + 1 + "/" + nowDate.getDate() + "/" + nowDate.getFullYear();
    let currentDate = nowDate.getMonth() + 1 + "/" + nowDate.getDate() + "/" + nowDate.getFullYear();
    let minMax = 0;

    let equationTypes = [
        { text: 'Linear', value: 'Linear' },
        { text: 'Exponential', value: 'Exponential' },
        { text: 'Logistic', value: 'Logistic' }
    ];
    let selectedEquationType = equationTypes[0].value;

    let paramMethods = [
        'Input Current Value and growth/decay rate (R)',
        'Input initial value, buy date, current value, and current date',
        'Input current value, and have an AI-suggested R value'
    ];
    let selectedParamMethod = paramMethods[0];

    let currentStep = 0;

    function nextStep() {
        if(currentStep == 0 && !assetType)
            return;
        else if(currentStep == 1 && !assetName)
            return;
        currentStep += 1;
    }

    function prevStep() {
        currentStep -= 1;
    }

    function closeModal() {
        open = false;
        resetForm();
    }

    function resetForm() {
        assetType = "";
        assetName = "";
        currentValue = 0;
        growthRateR = 0;
        initialValue = 0;
        buyDate = "";
        currentDate = "";
        selectedEquationType = equationTypes[1].value;
        selectedParamMethod = paramMethods[0];
        currentStep = 0;
    }



    function calculateLogisticR(initial_value, buy_date, current_value, current_date, min_max_value) {
		return ((Math.log(((min_max_value / current_value))/(initial_value))) / yearDifference(current_date, buy_date)) * -1
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

    function calculateLinearR(initial_value, buy_date, current_value, current_date) {
        if(currentDate == buy_date){
            return 1;
        }
  		return (current_value - initial_value) / yearDifference(current_date, buy_date);
	}


    function calculateExponentialR(initial_value, buy_date, current_value, current_date) {
    if (current_date === buy_date) {
        return 1;
    }
    
    let difference = yearDifference(current_date, buy_date);
    
    if (difference === 1) {
        return Math.log(current_value/initial_value) - 1; 
    }
    return (Math.log(current_value/initial_value) / Math.log(difference)) - 1;
}


    function yearDifference(year1, year2){
        year1 = new Date(year1);
        year2 = new Date(year2);
        return (year1 - year2) / (1000*60*60*24) / 365
    }

    async function submitForm(){
        open = false;
        const date = new Date();
        const todayDate = date.getMonth() + 1 + "/" + date.getDate() + "/" + date.getFullYear();
        let asset = {
            "asset_name": assetName,
            "asset_type": assetType,
            "function_type": selectedEquationType,
            "initial_value": 0,
            "min_max_value": minMax,
            "r": 0,
            "starting_date": ""
        }
        //current value and growth rate
        if(selectedParamMethod == paramMethods[0]){
            asset['initial_value'] = currentValue;
            asset['r'] = growthRateR;
            asset['starting_date'] = todayDate;
        }
        //initial value, buy date, current value, and current date
        else if(selectedParamMethod == paramMethods[1]){
            asset['initial_value'] = initialValue;
            if(selectedEquationType == 'Exponential'){
                asset['r'] = calculateExponentialR(initialValue, buyDate, currentValue, todayDate);
            }
            else if(selectedEquationType == 'Logistic'){
                asset['r'] = calculateLogisticR(initialValue, buyDate, currentValue, todayDate, minMax);
            }
            else if(selectedEquationType == 'Linear'){
                asset['r'] = calculateLinearR(initialValue, buyDate, currentValue, todayDate);
            }
            asset['starting_date'] = buyDate;
        }
        //Input current value, and have an AI-suggested R value
        else if(selectedParamMethod == paramMethods[2]){
            asset['initial_value'] = currentValue;
            asset['r'] = await suggestRValue(assetName + " of type " + assetType, selectedEquationType);
            asset['function_type'] = 'Exponential';
            asset['starting_date'] = todayDate;
        }

        const userData = $user;
        userData['assets'].push(asset);
        $user = userData;
        console.log($user)
    }
</script>

<style>
    .custom-label {
        display: block;
        margin-bottom: 10px;
    }

    fieldset {
        border: none;
        padding: 0;
    }

    input[type="radio"] {
        margin-right: 8px;
    }

    .button-group {
        margin-top: 20px;
    }
</style>

<button on:click={() => open = true}>Add Asset</button>

<Modal 
    bind:open 
    modalHeading="Asset Details" 
    on:click:button--secondary={closeModal}
    on:close={closeModal}
	passiveModal
>
    <Form>
        {#if currentStep === 0}
            <TextInput bind:value={assetType} placeholder="Enter asset type (e.g. house, car)" />
        {:else if currentStep === 1}
            <TextInput bind:value={assetName} placeholder="Enter the name of your asset" />
        {:else if currentStep === 2}
            <label class="custom-label" for="equationSelect">
                Select an equation type:
                <select id="equationSelect" bind:value={selectedEquationType}>
                    {#each equationTypes as type}
                        <option value={type.value}>{type.text}</option>
                    {/each}
                </select>
            </label>
        {:else if currentStep === 3}
            <fieldset>
                <legend>Select parameter method:</legend>
                {#each paramMethods as method, index}
                    <label class="custom-label">
                        <input type="radio" bind:group={selectedParamMethod} value={method} />
                        {method}
                    </label>
                {/each}
            </fieldset>
        {:else if currentStep === 4}
            {#if selectedParamMethod === paramMethods[0]}
                <p>Enter current value</p>
                <NumberInput bind:value={currentValue}/>
                {#if selectedEquationType == "Linear"}
                    <p>Enter yearly grow/decay rate:</p>
                {:else if selectedEquationType == "Exponential"}
                    <p>Enter growth/decay rate(R) [+ for growth] [- for decay]</p>
                {:else if selectedEquationType == "Logistic"}
                    <p>Enter growth/decay rate(R) [+ for growth] [- for decay]</p>
                {/if}
                <NumberInput bind:value={growthRateR}/>
                {#if selectedEquationType == "Logistic"}
                    <p>Enter min/max value for curve</p>
                    <NumberInput bind:value={minMax}/>
                {/if}
            {:else if selectedParamMethod === paramMethods[1]}
                <p>Enter initial value</p>
                <NumberInput bind:value={initialValue}/>
                <p>Enter buy date (MM/DD/YYYY)</p>
                <TextInput bind:value={buyDate}/>
                <p>Enter current value</p>
                <NumberInput bind:value={currentValue}/>
                {#if selectedEquationType == "Logistic"}
                    <p>Enter min/max value for curve</p>
                    <NumberInput bind:value={minMax}/>
                {/if}
            {:else}
                <p>Enter current value</p>
                <NumberInput bind:value={currentValue}/>
                <!-- AI-suggested R can be displayed here -->
                <!-- AI should also suggest min/max value -->
            {/if}
        {:else if currentStep === 5}
            <!-- Display custom equation -->
            <!-- Display graph -->
            <p>Asset Name: {assetName}</p>
            <p>Asset Type: {assetType}</p>
        {/if}
        
        <div class="button-group">
            {#if currentStep > 0}
                <Button on:click={prevStep}>Back</Button>
            {/if}
            {#if currentStep < 5}
                <Button on:click={nextStep}>Next</Button>
            {/if}
            {#if currentStep === 5}
                <Button on:click={submitForm}>Confirm</Button>
            {/if}
            <Button on:click={closeModal}>Cancel</Button>
        </div>
    </Form>
</Modal>
