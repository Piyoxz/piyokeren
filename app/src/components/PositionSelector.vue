<template>
  <v-container class="centered-container">
    <v-row justify="center">
      <v-col cols="12" sm="10" md="8">
        <!-- Dropdown for Position Selection -->
        <v-select
          v-model="selectedPosition"
          :items="positions"
          item-text="name"
          item-value="id"
          label="Pilih Posisi Pekerjaan"
          @change="fetchPhrases"
          outlined
        ></v-select>

        <!-- Display Phrases Based on Selected Position -->
        <v-card v-if="phrases.length > 0" class="mt-4">
          <v-card-title>
            Rekomendasi Frasa untuk {{ selectedPositionName }}
          </v-card-title>
          <v-divider></v-divider>
          <v-card-text>
            <v-chip
              v-for="(phrase, index) in phrases"
              :key="index"
              class="ma-2"
              outlined
            >
              {{ phrase }}
            </v-chip>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import axios from "axios";
const API_BASE_URL = "/api";

export default {
  data() {
    return {
      positions: [],
      selectedPosition: null,
      phrases: [],
    };
  },
  computed: {
    selectedPositionName() {
      const position = this.positions.find(
        (pos) => pos.id === this.selectedPosition
      );
      return position ? position.name : "";
    },
  },
  async mounted() {
    this.positions = await this.getPositions();
  },
  methods: {
    async getPositions() {
      const response = await axios.get(`${API_BASE_URL}/positions`);
      return response.data.positions;
    },
    async fetchPhrases() {
      if (!this.selectedPosition) return;
      const response = await axios.get(`${API_BASE_URL}/position_phrases`, {
        params: { position: this.selectedPosition },
      });
      this.phrases = response.data.phrases;
    },
  },
};
</script>

<style scoped>
.centered-container {
  margin-top: 30px;
}
</style>
