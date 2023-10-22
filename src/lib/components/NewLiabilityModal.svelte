<script>
    import { Button, Modal, TextInput } from "carbon-components-svelte";
    
    let open = false;
    let liabilityValue = '';
  </script>
    
  <Button on:click={() => (open = true)}>Add Liability</Button>
    
  <Modal
    bind:open
    modalHeading="Add Liability"
    primaryButtonText="Confirm"
    secondaryButtonText="Cancel"
    on:click:button--secondary={() => (open = false)}
    on:open
    on:close
    on:submit={() => {
      console.log(liabilityValue);
      open = false;
    }}
  >
    <TextInput
      id="liabilityValue"
      labelText="Liability Value"
      value={liabilityValue}
      on:input={(event) => {
        liabilityValue = event.target.value;
      }}
    />
  </Modal>