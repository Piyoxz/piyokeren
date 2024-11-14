<template>
  <v-container>
    <v-dialog v-model="showDialog" persistent max-width="450">
      <v-card class="elevation-12 dialog-card">
        <!-- Card Header with Icon and Title -->
        <v-card-title class="text-center justify-center">
          <v-avatar size="64" color="purple">
            <v-icon size="36">mdi-account-circle</v-icon>
          </v-avatar>
        </v-card-title>

        <v-card-subtitle class="text-center dialog-title mt-2">
          Daftar Piyo
        </v-card-subtitle>

        <v-card-text>
          <p class="text-center dialog-description">
            Masukkan nama Anda untuk melanjutkan
          </p>
          <v-text-field
            v-model="nameInput"
            label="Nama Anda"
            outlined
            dense
            color="purple"
            :rules="[nameRules]"
            autofocus
            class="dialog-input"
          ></v-text-field>
        </v-card-text>

        <!-- Card Actions with Centered Button -->
        <v-card-actions class="justify-center">
          <v-btn
            color="purple"
            @click="saveName"
            :disabled="!nameInput || loading"
            rounded
            large
            class="dialog-button"
          >
            <v-icon left>mdi-check-circle</v-icon>
            <span v-if="!loading">Lanjutkan</span>
            <span v-else>Lagi proses...</span>
          </v-btn>
        </v-card-actions>
        <v-alert v-if="error" type="error" dense text class="mt-2">
          {{ error }}
        </v-alert>
      </v-card>
    </v-dialog>
  </v-container>
</template>

<script>
import { daftarPiyomyid } from "@/services/api";
export default {
  name: "RegisterPage",
  data() {
    return {
      showDialog: false, // controls dialog visibility
      nameInput: "", // holds the user's input
      userName: "", // stores and displays the user's name
      loading: false, // loading indicator for API call
      error: null, // error message
    };
  },

  computed: {
    nameRules() {
      return (v) => !!v || "Nama wajib diisi";
    },
  },

  methods: {
    async saveName() {
      // Set loading and reset error
      this.loading = true;
      this.error = null;

      try {
        const userData = {
          id: new Date().getTime().toString(),
          name: this.nameInput,
        };
        await daftarPiyomyid(userData);

        localStorage.setItem("userName", this.nameInput);
        localStorage.setItem("userId", userData.id);
        this.userName = this.nameInput;
        this.showDialog = false;

        this.$router.push("/");
      } catch (error) {
        this.error = "Gagal mendaftarkan, coba lagi.";
      } finally {
        this.loading = false;
      }
    },
  },

  mounted() {
    // Check localStorage for an existing name
    const storedName = localStorage.getItem("userName");
    if (storedName) {
      this.userName = storedName;
    } else {
      this.showDialog = true; // Open dialog if no name is stored
    }
  },
};
</script>


<style scoped>
.dialog-card {
  border-radius: 16px;
  padding-top: 20px;
}

.dialog-title {
  font-size: 1.5rem;
  font-weight: 600;
  color: #5e35b1; /* Purple color for title */
  margin-top: -10px;
}

.dialog-description {
  font-size: 1rem;
  color: #666;
}

.dialog-input {
  margin-top: 15px;
}

.dialog-button {
  background-color: #5e35b1;
  color: white;
  width: 100%;
  max-width: 250px;
}

.dialog-button:disabled {
  background-color: #d1c4e9;
}

.v-avatar {
  box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.1);
}
</style>
