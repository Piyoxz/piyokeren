<template>
  <v-container>
    <h1>Edit Item</h1>
    <v-form>
      <v-text-field label="Name" v-model="name"></v-text-field>
      <v-text-field label="Description" v-model="description"></v-text-field>
      <v-btn color="primary">Save Changes</v-btn>
    </v-form>
  </v-container>
</template>

<script>
export default {
  name: "EditPage",
  data() {
    return {
      name: 'Existing Item Name', // Placeholder for pre-filled data
      description: 'Existing Item Description',
    };
  },
};
</script>
