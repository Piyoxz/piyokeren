<template>
  <v-container>
    <!-- Top bar with page title and Add button -->
    <div class="d-flex justify-space-between align-center mb-4">
      <h1 class="page-title">Daftar CV</h1>
      <v-btn
        v-if="cvList.length"
        color="success"
        @click="showDialog = true"
        class="add-btn"
      >
        <v-icon left>mdi-plus</v-icon> Tambah CV
      </v-btn>
    </div>

    <!-- Dialog for File Name Input -->
    <v-dialog v-model="showDialog" max-width="400px">
      <v-card>
        <v-card-title class="text-h6">Masukkan Nama File CV</v-card-title>
        <v-card-text>
          <v-text-field
            v-model="fileName"
            label="Nama File"
            :rules="fileNameRules"
            placeholder="Masukkan nama file (tanpa spasi atau simbol)"
            outlined
          ></v-text-field>
          <v-alert v-if="errorMessage" type="error" class="mt-2" dense>
            {{ errorMessage }}
          </v-alert>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn text @click="showDialog = false">Batal</v-btn>
          <v-btn color="success" @click="submitFileName" :disabled="!fileName">
            Tambah
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <!-- CV Cards Grid if there are CVs in the list -->
    <div v-if="cvList.length > 0">
      <v-row>
        <v-col
          v-for="cv in cvList"
          :key="cv.id"
          cols="12"
          sm="6"
          md="4"
          lg="3"
          class="mb-4"
        >
          <v-card class="cv-card hover-effect" elevation="10">
            <v-img
              src="https://i.pinimg.com/736x/ff/89/f1/ff89f12c12b563078d4fe062157256ad.jpg"
              height="180px"
              cover
              class="cv-card-image rounded-image"
            ></v-img>

            <v-card-title class="cv-card-title text-h6 font-weight-bold">
              {{ cv.fileName }}
            </v-card-title>
            <v-card-subtitle class="cv-card-subtitle text-body-2 grey--text">
              {{ formatTime(cv.createdAt) }}
            </v-card-subtitle>

            <v-divider></v-divider>

            <v-card-actions class="justify-space-between">
              <v-btn small color="primary" @click="editCV(cv.id)">
                <v-icon left>mdi-pencil</v-icon>Edit
              </v-btn>
              <v-btn small color="red darken-2" @click="deleteCV(cv.id)">
                <v-icon left>mdi-delete</v-icon>Delete
              </v-btn>
              <v-btn small color="success darken-2" @click="generateCV(cv)">
                <v-icon left>mdi-file-pdf</v-icon>PDF
              </v-btn>
            </v-card-actions>
          </v-card>
        </v-col>
      </v-row>
    </div>

    <!-- Empty State when no CVs are available -->
    <div v-else class="empty-state">
      <h2 class="empty-title">Belum ada CV yang dibuat</h2>
      <v-btn color="success" @click="showDialog = true" class="add-btn-large">
        <v-icon left>mdi-plus</v-icon> Tambah CV
      </v-btn>
    </div>
  </v-container>
</template>

<script>
import { saveCv, getCvs, deleteCv, generateCv } from "@/services/api"; // Make sure the path to your API file is correct

export default {
  name: "IndexPage",

  created() {
    this.userId = localStorage.getItem("userId");
  },

  data() {
    return {
      showDialog: false,
      fileName: "",
      errorMessage: "",
      cvList: [],
      userId: "",
    };
  },

  computed: {
    // Validation rules for the file name input
    fileNameRules() {
      return [
        (v) => !!v || "Nama file wajib diisi",
        (v) =>
          /^[\w-]+$/.test(v) ||
          "Nama file hanya boleh menggunakan huruf, angka, tanda hubung (-), atau garis bawah (_)",
      ];
    },
  },

  methods: {
    // Fetch CVs for the user when the component is created
    async fetchCvs() {
      try {
        this.cvList = await getCvs(this.userId); // Fetch CVs by userId
      } catch (error) {
        console.error("Error fetching CVs:", error);
      }
    },

    editCV(id) {
      this.$router.push({ path: "/add", query: { id } });
    },

    async deleteCV(id) {
      if (confirm("Are you sure you want to delete this CV?")) {
        this.cvList = this.cvList.filter((cv) => cv.id !== id);
        await deleteCv(id);
        this.$toast.success("CV berhasil dihapus!");
        this.fetchCvs();
      }
    },

    formatTime(time) {
      const date = new Date(time);
      return date.toLocaleDateString("id-ID", {
        day: "2-digit",
        month: "long",
        year: "numeric",
      });
    },

    async generateCV(data) {
      try {
        const response = await generateCv({
          cvData: data,
        });

        // Download file
        const link = document.createElement("a");
        link.href = response.path;
        link.download = "CV.pdf";
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);

        this.$toast.success("CV berhasil di-generate!");
        this.loading = false;

        await new Promise((resolve) => setTimeout(resolve, 1000));
        this.$router.push("/");
      } catch (error) {
        this.$toast.error("Gagal men-generate CV. Silakan coba lagi.");
        console.error("Error generating CV:", error);
        this.loading = false;
      }
    },

    // Handle the submission of the file name to create a new CV
    async submitFileName() {
      if (!/^[\w-]+$/.test(this.fileName)) {
        this.errorMessage =
          "Nama file tidak boleh mengandung spasi atau simbol";
      } else {
        this.errorMessage = "";

        const newCvData = {
          id: new Date().getTime().toString(),
          name: this.fileName,
          userId: this.userId,
        };

        try {
          await saveCv(newCvData);
          this.cvList.push(newCvData);
          this.showDialog = false;
          this.$router.push({
            path: "/add",
            query: { id: newCvData.id },
          });
        } catch (error) {
          console.error("Error saving CV:", error);
          this.errorMessage = "Gagal menyimpan CV. Coba lagi nanti.";
        }
      }
    },
  },

  mounted() {
    this.fetchCvs(); // Fetch CVs when component mounts
  },
};
</script>

<style scoped>
.page-title {
  font-size: 2rem;
  font-weight: 700;
  color: #2e4053;
}

.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 60vh;
  text-align: center;
}

.empty-title {
  font-size: 1.5rem;
  color: #707b7c;
  margin-bottom: 20px;
}

.add-btn-large {
  font-weight: 600;
  color: white;
  background-color: #2e8b57;
  box-shadow: 0px 4px 12px rgba(46, 139, 87, 0.4);
  padding: 10px 20px;
}

.add-btn-large:hover {
  background-color: #3cb371;
  box-shadow: 0px 6px 16px rgba(46, 139, 87, 0.6);
}

.add-btn {
  align-self: center;
  font-weight: 600;
  color: white;
  background-color: #2e8b57;
  box-shadow: 0px 4px 12px rgba(46, 139, 87, 0.4);
}

.add-btn:hover {
  background-color: #3cb371;
  box-shadow: 0px 6px 16px rgba(46, 139, 87, 0.6);
}

.cv-card {
  border-radius: 12px;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.cv-card:hover {
  transform: translateY(-5px);
  box-shadow: 0px 8px 20px rgba(0, 0, 0, 0.15);
}

.cv-card-title {
  font-weight: 700;
  padding: 10px 16px;
  text-align: center;
}

.cv-card-subtitle {
  color: #757575;
  text-align: center;
}

.cv-card-image {
  border-radius: 12px 12px 0 0;
  overflow: hidden;
}

.cv-card-actions {
  padding: 8px;
}

.hover-effect:hover .cv-card-image {
  opacity: 0.85;
}
</style>
