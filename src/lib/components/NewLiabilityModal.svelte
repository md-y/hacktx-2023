<script>
    import { Form, Button, Modal, TextInput } from "carbon-components-svelte";
    
    let open = false;
    let liabilityValue = 0;

    function closeModal() {
        open = false;
        resetForm();
    }
    function resetForm() {
        liabilityValue = 0;
    }

    async function submitForm() {
        const date = new Date();
        const todayDate = date.getMonth() + 1 + "/" + date.getDate() + "/" + date.getFullYear();
        let bill = {
            "payment_amount": liabilityValue,
            "payment_date": todayDate
        }

        bill["payment_amount"] = liabilityValue;
    }
  </script>
    
  <Button on:click={() => (open = true)}>Add Liability</Button>
    
  <Modal
    bind:open
    modalHeading="Add Liability"
    on:click:button--secondary={closeModal}
    on:close={closeModal}
	passiveModal
  >

    <Form>
        <TextInput
            id="liabilityValue"
            labelText="Liability Value"
            value={liabilityValue}
            on:input={(event) => {
                liabilityValue = event.target.value;
            }}
        />
        <div class ="button-group">
            <Button on:click={closeModal}>Cancel</Button>
            <Button on:click={()=>{submitForm(); closeModal();}}>Confirm</Button>
        </div>
    </Form>
  </Modal>