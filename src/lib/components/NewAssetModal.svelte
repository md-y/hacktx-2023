<script>
    import { Modal, Form, TextInput, Dropdown, Button } from 'carbon-components-svelte';
    export let open = false;

    let assetType = '';
    let assetName = '';
    let currentValue = '';
    let growthRateR = '';
    let initialValue = '';
    let buyDate = '';
    let currentDate = '';
    
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
        assetType = '';
        assetName = '';
        selectedEquationType = equationTypes[0].value;
        selectedParamMethod = paramMethods[0];
        currentStep = 0;
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
</style>

<button on:click={() => open = true}>Add Asset</button>

<Modal 
    bind:open 
    modalHeading="Asset Details" 
    on:click:button--secondary={closeModal}
    on:close={closeModal}
>
    <Form>
        {#if currentStep === 0}
            <TextInput bind:value={assetType} placeholder="Enter asset type (e.g. house, car)" />
        {:else if currentStep === 1}
            <TextInput bind:value={assetName} placeholder="Enter the name of your asset" />
        {:else if currentStep === 2}
            <label class="custom-label">
                Select an equation type:
                <select bind:value={selectedEquationType}>
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
                <TextInput bind:value={currentValue} placeholder="Enter current value" />
                <TextInput bind:value={growthRateR} placeholder="Enter growth/decay rate (R)" />
            {:else if selectedParamMethod === paramMethods[1]}
                <TextInput bind:value={initialValue} placeholder="Enter initial value" />
                <TextInput bind:value={buyDate} placeholder="Enter buy date" />
                <TextInput bind:value={currentValue} placeholder="Enter current value" />
                <TextInput bind:value={currentDate} placeholder="Enter current date" />
            {:else}
                <TextInput bind:value={currentValue} placeholder="Enter current value" />
                <!-- AI-suggested R can be displayed here -->
            {/if}
        {:else if currentStep === 5}
            <!-- Display custom equation -->
            <!-- Display graph -->
        {/if}
        
        <div class="button-group">
            {#if currentStep > 0}
                <Button on:click={prevStep}>Back</Button>
            {/if}
            {#if currentStep < 5}
                <Button on:click={nextStep}>Next</Button>
            {/if}
            {#if currentStep === 5}
                <Button on:click={closeModal}>Confirm</Button>
            {/if}
            <Button on:click={closeModal}>Cancel</Button>
        </div>
    </Form>
</Modal>
