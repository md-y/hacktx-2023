<script>
	// @ts-nocheck

	import { Modal, Form, TextInput } from 'carbon-components-svelte';
	export let open;
</script>

<Modal
	bind:open
	modalHeading="Create database"
	primaryButtonText="Confirm"
	secondaryButtonText="Cancel"
	on:click:button--secondary={() => (open = false)}
	on:open
	on:close
	on:submit
>
	<Form>
		<TextInput id="asset-name" />
	</Form>
</Modal>
