<script>
	import { user } from '$lib/store';
	import { Form, Button, Modal, TextInput } from 'carbon-components-svelte';

	export let open = false;
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
		const todayDate = date.getMonth() + 1 + '/' + date.getDate() + '/' + date.getFullYear();
		let bill = {
			payment_amount: liabilityValue,
			payment_date: todayDate
		};

		user.set({
			...$user,
			bills: $user.bills.concat([bill])
		});
	}
</script>

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
			bind:value={liabilityValue}
			type="number"
		/>
		<div class="button-group">
			<Button on:click={closeModal}>Cancel</Button>
			<Button
				on:click={() => {
					submitForm();
					closeModal();
				}}>Confirm</Button
			>
		</div>
	</Form>
</Modal>
