<template>
  <v-container class="centered-container">
    <v-app-bar color="primary" dark>
      <!-- Back Button -->
      <v-btn icon @click="$router.go(-1)">
        <v-icon>mdi-arrow-left</v-icon>
      </v-btn>

      <!-- Centered Title -->
      <v-toolbar-title class="text-center">
        {{ fileName || form.fileName || "Nama File" }}
      </v-toolbar-title>
    </v-app-bar>
    <v-snackbar
      v-model="showNotification"
      color="green"
      timeout="3000"
      top
      right
      elevation="6"
    >
      <v-icon left dark>mdi-check-circle</v-icon>
      Data berhasil diupdate!
    </v-snackbar>
    <v-row justify="center">
      <v-col cols="12" sm="10" md="8">
        <!-- Each section in a card -->
        <v-card
          v-for="(section, index) in sections"
          :key="index"
          class="mb-4 custom-card"
          :class="{ 'expanded-card': expandedSection === index }"
          outlined
        >
          <!-- Card Header to mimic the look of the sections -->
          <div class="card-header">
            <!-- Left section for the icon and title -->
            <div class="flex-grow-1">
              <v-icon left class="header-icon">{{ section.icon }}</v-icon>
              <span class="header-title">{{ section.title }}</span>
            </div>

            <!-- Right section for the expand/collapse button -->
            <v-btn
              icon
              @click="toggleSection(index)"
              style="background-color: transparent"
              flat
              tile
            >
              <v-icon>{{
                expandedSection === index
                  ? "mdi-chevron-up"
                  : "mdi-chevron-down"
              }}</v-icon>
            </v-btn>
          </div>

          <!-- Card Content for each section; shown only if expanded -->
          <div v-if="expandedSection === index" class="card-content">
            <div v-if="section.title === 'Objektif'">
              <v-icon class="info-icon" color="blue"
                >mdi-information-outline</v-icon
              >
              <p class="info-text">
                Deskripsikan latar belakangmu, seperti pendidikan, pengalaman
                karir atau ketertarikan yang relevan dengan kualifikasi
                pekerjaan yang dilamar.
              </p>
              <label>Deskripsi <span class="required-star">*</span></label>
              <div class="quill-editor-container">
                <!-- Rekomendasi Frasa Text in Position Absolute -->
                <div class="rekomendasi-frasa">
                  <v-btn
                    width="128"
                    class="white--text text-capitalize font-weight-regular"
                    depressed
                    style="background-color: transparent"
                    flat
                    tile
                    @click="openDialogRekomendasiFrasaPekerjaan"
                  >
                    <v-icon left color="blue">mdi-lightbulb</v-icon>
                    <div class="ms-2" style="font-size: 14px; color: blue">
                      Rekomendasi Frasa
                    </div>
                  </v-btn>
                </div>

                <!-- Quill Editor for description -->
                <QuillEditor
                  ref="objektif"
                  :options="quillOptions"
                  style="height: 200px"
                  scrollingContainer
                  @textChange="onEditorInput"
                />
              </div>

              <div v-if="dialog.rekomendasiFrasaPekerjaan">
                <v-card class="floating-card" elevation="8" max-width="400">
                  <v-card-title class="d-flex justify-space-between">
                    <span>Rekomendasi Frasa</span>
                    <v-btn
                      flat
                      tile
                      icon
                      @click="closeDialogRekomendasiFrasaPekerjaan"
                    >
                      <v-icon>mdi-close</v-icon>
                    </v-btn>
                  </v-card-title>

                  <v-card-text>
                    <v-text-field
                      v-model="searchQuery"
                      label="Cari..."
                      prepend-inner-icon="mdi-magnify"
                      clearable
                      outlined
                      dense
                      hide-details
                      class="mb-2"
                    ></v-text-field>

                    <div style="height: 300px; overflow-y: auto">
                      <template v-if="pekerjaanForm.position === null">
                        <v-list dense>
                          <v-list-item
                            v-for="(job, index) in filteredJobs"
                            :key="index"
                            @click="selectPosition(job)"
                            class="job-item"
                            link
                          >
                            <v-list-item-content>
                              <v-list-item-title class="text-subtitle-2">{{
                                job
                              }}</v-list-item-title>
                            </v-list-item-content>
                          </v-list-item>
                        </v-list>
                      </template>

                      <!-- List frasa setelah pilih pekerjaan -->
                      <template v-else>
                        <v-list dense>
                          <v-list-item
                            v-for="(phrase, ix) in filteredPhrases"
                            :key="ix"
                            @click="selectPhrase(phrase)"
                            class="phrase-item"
                            link
                          >
                            <v-list-item-content>
                              <v-list-item-title class="text-subtitle-2">{{
                                phrase
                              }}</v-list-item-title>
                            </v-list-item-content>
                          </v-list-item>
                        </v-list>
                      </template>
                    </div>
                  </v-card-text>
                </v-card>
              </div>
            </div>
            <div v-if="section.title === 'Informasi Pribadi'">
              <v-text-field
                label="Nama Lengkap"
                v-model="form.personalInfo.namaLengkap"
                outlined
                required
              ></v-text-field>

              <v-row>
                <v-col cols="12" md="6">
                  <v-text-field
                    label="Email"
                    v-model="form.personalInfo.email"
                    outlined
                    required
                  ></v-text-field>
                </v-col>
                <v-col cols="12" md="6">
                  <v-text-field
                    label="Nomor HP"
                    v-model="form.personalInfo.nomorHp"
                    outlined
                    required
                  ></v-text-field>
                </v-col>
              </v-row>

              <v-text-field
                label="URL Profil LinkedIn"
                v-model="form.personalInfo.linkedinUrl"
                outlined
              ></v-text-field>

              <v-text-field
                label="URL Portofolio/Situs Web (Opsional)"
                v-model="form.personalInfo.portofolioUrl"
                outlined
              ></v-text-field>

              <v-textarea
                label="Alamat"
                v-model="form.personalInfo.alamat"
                outlined
                required
              ></v-textarea>
            </div>

            <div v-if="section.title === 'Riwayat Pendidikan'">
              <v-alert
                type="info"
                border="left"
                prominent
                text
                color="blue lighten-4"
                class="mb-4"
              >
                <v-icon left color="blue">mdi-information-outline</v-icon>
                Lebih baik cantumkan riwayat pendidikan terakhirmu saja untuk
                tampilan CV yang lebih baik!
              </v-alert>

              <div
                v-for="(education, index) in form.educationHistory"
                :key="index"
                class="education-entry mb-4"
              >
                <v-card outlined class="form-field-card">
                  <v-card-title class="d-flex align-center">
                    Riwayat Pendidikan {{ index + 1 }}
                    <v-spacer></v-spacer>
                    <v-btn
                      icon
                      color="red"
                      style="background-color: transparent"
                      flat
                      tile
                      width="28"
                      height="28"
                      @click="removeEducationEntry(index)"
                    >
                      <v-icon>mdi-delete</v-icon>
                    </v-btn>
                  </v-card-title>

                  <v-card-text>
                    <v-row>
                      <v-col cols="12" md="6">
                        <v-text-field
                          v-model="education.institution"
                          label="Nama Sekolah/Universitas"
                          outlined
                          required
                        ></v-text-field>
                      </v-col>
                      <v-col cols="12" md="6">
                        <v-text-field
                          v-model="education.location"
                          label="Lokasi"
                          outlined
                          required
                        ></v-text-field>
                      </v-col>
                    </v-row>

                    <v-row>
                      <v-col cols="6">
                        <v-autocomplete
                          v-model="education.startYear"
                          :items="tahun"
                          label="Tahun Mulai"
                          outlined
                          required
                        ></v-autocomplete>
                      </v-col>
                      <v-col cols="6">
                        <v-autocomplete
                          v-model="education.endYear"
                          :items="tahun"
                          label="Tahun Selesai"
                          outlined
                          :disabled="education.currentlyStudying"
                          required
                        ></v-autocomplete>
                      </v-col>
                    </v-row>

                    <v-row>
                      <v-col cols="12" md="6">
                        <v-select
                          v-model="education.educationLevel"
                          :items="educationLevels"
                          label="Tingkat Pendidikan"
                          outlined
                          required
                        ></v-select>
                      </v-col>
                      <v-col cols="12" md="6">
                        <v-text-field
                          v-model="education.program"
                          label="Program Pendidikan"
                          outlined
                          required
                        ></v-text-field>
                      </v-col>
                    </v-row>

                    <v-row>
                      <v-col cols="6">
                        <v-text-field
                          v-model="education.gpa"
                          label="IPK (Opsional namun direkomendasikan)"
                          outlined
                        ></v-text-field>
                      </v-col>
                      <v-col cols="6">
                        <v-text-field
                          v-model="education.maxGpa"
                          label="IPK Maksimal"
                          outlined
                        ></v-text-field>
                      </v-col>
                    </v-row>

                    <label>Deskripsi</label>
                    <p class="caption mb-2">
                      Jelaskan prestasi, kontribusi, atau projek penelitian kamu
                      selama pendidikan
                    </p>
                    <div class="quill-editor-container mb-4">
                      <div class="rekomendasi-frasa">
                        <v-btn
                          width="128"
                          class="white--text text-capitalize font-weight-regular"
                          depressed
                          style="background-color: transparent"
                          flat
                          tile
                          @click="openDialogRekomendasiFrasaPendidikan"
                        >
                          <v-icon left color="blue">mdi-lightbulb</v-icon>
                          <div
                            class="ms-2"
                            style="font-size: 14px; color: blue"
                          >
                            Rekomendasi Frasa
                          </div>
                        </v-btn>
                      </div>

                      <QuillEditor
                        :ref="'educationDescription' + index"
                        v-model="education.description"
                        :options="quillOptions"
                        style="height: 150px"
                        scrollingContainer
                        @textChange="onEducationDescriptionChange(index)"
                      />
                    </div>

                    <v-switch
                      v-model="education.currentlyStudying"
                      label="Saat ini saya masih belajar di sini"
                      color="green"
                      inset
                    ></v-switch>

                    <div v-if="dialog.rekomendasiFrasaPendidikan">
                      <v-card
                        class="floating-card-pendidikan"
                        elevation="8"
                        max-width="400"
                      >
                        <v-card-title class="d-flex justify-space-between">
                          <span>Rekomendasi Frasa</span>
                          <v-btn
                            flat
                            tile
                            icon
                            @click="closeDialogRekomendasiFrasaPendidikan"
                          >
                            <v-icon>mdi-close</v-icon>
                          </v-btn>
                        </v-card-title>

                        <v-card-text>
                          <v-text-field
                            v-model="searchQuery"
                            label="Cari..."
                            prepend-inner-icon="mdi-magnify"
                            clearable
                            outlined
                            dense
                            hide-details
                            class="mb-2"
                          ></v-text-field>

                          <div style="height: 300px; overflow-y: auto">
                            <template v-if="pendidikanForm.level === null">
                              <v-list dense>
                                <v-list-item
                                  v-for="(level, index) in pendidikanForm.data"
                                  :key="index"
                                  @click="selectLevel(level)"
                                  class="level-item"
                                  link
                                >
                                  <v-list-item-content>
                                    <v-list-item-title
                                      class="text-subtitle-2"
                                      >{{ level }}</v-list-item-title
                                    >
                                  </v-list-item-content>
                                </v-list-item>
                              </v-list>
                            </template>

                            <template v-else-if="pendidikanForm.field === null">
                              <v-list dense>
                                <v-list-item
                                  v-for="(field, index) in pendidikanForm.data"
                                  :key="index"
                                  @click="selectField(field)"
                                  class="field-item"
                                  link
                                >
                                  <v-list-item-content>
                                    <v-list-item-title
                                      class="text-subtitle-2"
                                      >{{ field }}</v-list-item-title
                                    >
                                  </v-list-item-content>
                                </v-list-item>
                              </v-list>
                            </template>

                            <template v-else>
                              <v-list dense>
                                <v-list-item
                                  v-for="(
                                    phrase, ix
                                  ) in filteredPhrasesPendidikan"
                                  :key="ix"
                                  @click="selectPhrasePendidikan(phrase, index)"
                                  class="phrase-item"
                                  link
                                >
                                  <v-list-item-content>
                                    <v-list-item-title
                                      class="text-subtitle-2"
                                      >{{ phrase }}</v-list-item-title
                                    >
                                  </v-list-item-content>
                                </v-list-item>
                              </v-list>
                            </template>
                          </div>
                        </v-card-text>
                      </v-card>
                    </div>
                  </v-card-text>
                </v-card>
              </div>

              <div
                class="d-flex align-center"
                @click="addEducationEntry"
                style="cursor: pointer"
              >
                <v-btn
                  icon
                  color="green"
                  style="background-color: transparent"
                  flat
                  tile
                  width="28"
                  height="28"
                >
                  <v-icon left color="white">mdi-plus</v-icon>
                </v-btn>
                <span class="ms-2 blue--text"> Tambah Riwayat Pendidikan </span>
              </div>
            </div>

            <div v-if="section.title === 'Riwayat Pekerjaan'">
              <div
                v-for="(job, index) in form.workExperience"
                :key="index"
                class="job-entry mb-4"
              >
                <v-card outlined class="form-field-card">
                  <v-card-title class="d-flex align-center">
                    Riwayat Pekerjaan {{ index + 1 }}
                    <v-spacer></v-spacer>
                    <v-btn
                      icon
                      color="red"
                      style="background-color: transparent"
                      flat
                      tile
                      width="28"
                      height="28"
                      @click="removeJobEntry(index)"
                    >
                      <v-icon>mdi-delete</v-icon>
                    </v-btn>
                  </v-card-title>

                  <v-card-text>
                    <v-row>
                      <v-col cols="12">
                        <v-text-field
                          v-model="job.institution"
                          label="Nama Instansi"
                          outlined
                          required
                        ></v-text-field>
                      </v-col>
                    </v-row>

                    <v-row>
                      <v-col cols="12" md="6">
                        <v-text-field
                          v-model="job.position"
                          label="Jabatan/Bidang"
                          outlined
                          required
                        ></v-text-field>
                      </v-col>
                      <v-col cols="12" md="6">
                        <v-select
                          v-model="job.employeeStatus"
                          :items="employeeStatuses"
                          label="Status Karyawan"
                          outlined
                          required
                        ></v-select>
                      </v-col>
                    </v-row>

                    <v-row>
                      <v-col cols="12" md="4">
                        <v-text-field
                          v-model="job.startDate"
                          label="Mulai"
                          type="date"
                          outlined
                          required
                        ></v-text-field>
                      </v-col>

                      <v-col cols="12" md="4">
                        <v-text-field
                          v-model="job.endDate"
                          label="Selesai"
                          type="date"
                          outlined
                          :disabled="job.currentlyWorking"
                        ></v-text-field>
                      </v-col>

                      <v-col cols="12" md="4">
                        <v-text-field
                          v-model="job.location"
                          label="Lokasi"
                          outlined
                          required
                        ></v-text-field>
                      </v-col>
                    </v-row>

                    <label>Deskripsi</label>
                    <p class="caption mb-2">
                      Jelaskan hal yang kamu lakukan selama bekerja. Jelaskan
                      pencapaian kerjamu dengan angka agar lebih realistis!
                    </p>
                    <div class="quill-editor-container mb-4">
                      <div class="rekomendasi-frasa">
                        <v-btn
                          width="128"
                          class="white--text text-capitalize font-weight-regular"
                          depressed
                          style="background-color: transparent"
                          flat
                          tile
                          @click="openDialogRekomendasiFrasaPekerjaan2"
                        >
                          <v-icon left color="blue">mdi-lightbulb</v-icon>
                          <div
                            class="ms-2"
                            style="font-size: 14px; color: blue"
                          >
                            Rekomendasi Frasa
                          </div>
                        </v-btn>
                      </div>

                      <QuillEditor
                        :ref="'workExperienceDescription' + index"
                        v-model="job.description"
                        :options="quillOptions"
                        style="height: 150px"
                        scrollingContainer
                        @textChange="onWorkExperienceDescriptionChange(index)"
                      />
                    </div>

                    <v-switch
                      v-model="job.currentlyWorking"
                      label="Masih bekerja disini"
                      inset
                      colo
                    ></v-switch>

                    <div v-if="dialog.rekomendasiFrasaPekerjaan2">
                      <v-card
                        class="floating-card"
                        elevation="8"
                        max-width="400"
                      >
                        <v-card-title class="d-flex justify-space-between">
                          <span>Rekomendasi Frasa</span>
                          <v-btn
                            flat
                            tile
                            icon
                            @click="closeDialogRekomendasiFrasaPekerjaan"
                          >
                            <v-icon>mdi-close</v-icon>
                          </v-btn>
                        </v-card-title>

                        <v-card-text>
                          <v-text-field
                            v-model="searchQuery"
                            label="Cari..."
                            prepend-inner-icon="mdi-magnify"
                            clearable
                            outlined
                            dense
                            hide-details
                            class="mb-2"
                          ></v-text-field>

                          <div style="height: 300px; overflow-y: auto">
                            <template v-if="pekerjaanForm.position === null">
                              <v-list dense>
                                <v-list-item
                                  v-for="(job, index) in filteredJobs"
                                  :key="index"
                                  @click="selectPosition(job)"
                                  class="job-item"
                                  link
                                >
                                  <v-list-item-content>
                                    <v-list-item-title
                                      class="text-subtitle-2"
                                      >{{ job }}</v-list-item-title
                                    >
                                  </v-list-item-content>
                                </v-list-item>
                              </v-list>
                            </template>

                            <!-- List frasa setelah pilih pekerjaan -->
                            <template v-else>
                              <v-list dense>
                                <v-list-item
                                  v-for="(phrase, ix) in filteredPhrases"
                                  :key="ix"
                                  @click="selectPhrase2(phrase, index)"
                                  class="phrase-item"
                                  link
                                >
                                  <v-list-item-content>
                                    <v-list-item-title
                                      class="text-subtitle-2"
                                      >{{ phrase }}</v-list-item-title
                                    >
                                  </v-list-item-content>
                                </v-list-item>
                              </v-list>
                            </template>
                          </div>
                        </v-card-text>
                      </v-card>
                    </div>
                  </v-card-text>
                </v-card>
              </div>

              <div
                class="d-flex align-center"
                @click="addJobEntry"
                style="cursor: pointer"
              >
                <v-btn
                  icon
                  color="green"
                  style="background-color: transparent"
                  flat
                  tile
                  width="28"
                  height="28"
                >
                  <v-icon left color="white">mdi-plus</v-icon>
                </v-btn>
                <span class="ms-2 blue--text"> Tambah Riwayat Pekerjaan </span>
              </div>
            </div>

            <div v-if="section.title === 'Sertifikasi/Lisensi'">
              <div
                v-for="(certification, index) in form.certifications"
                :key="index"
                class="certification-entry mb-4"
              >
                <v-card
                  outlined
                  class="form-field-card mt-2"
                  elevation="8"
                  style="border: 1px solid #1e88e5"
                >
                  <v-card-title class="d-flex align-center">
                    Sertifikasi/Lisensi {{ index + 1 }}
                    <v-spacer></v-spacer>
                    <v-btn
                      icon
                      color="red"
                      style="background-color: transparent"
                      flat
                      tile
                      width="28"
                      height="28"
                      @click="removeCertificationEntry(index)"
                    >
                      <v-icon>mdi-delete</v-icon>
                    </v-btn>
                  </v-card-title>

                  <v-card-text>
                    <v-row>
                      <v-col cols="12" md="6">
                        <v-text-field
                          v-model="certification.name"
                          label="Nama Sertifikasi/Lisensi"
                          outlined
                          required
                        ></v-text-field>
                      </v-col>
                      <v-col cols="12" md="6">
                        <v-text-field
                          v-model="certification.issuer"
                          label="Penerbit Sertifikasi/Lisensi"
                          outlined
                          required
                        ></v-text-field>
                      </v-col>
                    </v-row>

                    <v-row>
                      <v-col cols="12" md="6">
                        <v-text-field
                          v-model="certification.number"
                          label="Nomor Sertifikasi/Lisensi"
                          outlined
                        ></v-text-field>
                      </v-col>
                      <v-col cols="12" md="6">
                        <v-autocomplete
                          v-model="certification.year"
                          :items="tahun"
                          label="Tahun Sertifikasi"
                          outlined
                          required
                        ></v-autocomplete>
                      </v-col>
                    </v-row>
                  </v-card-text>
                </v-card>
              </div>

              <div
                class="d-flex align-center"
                @click="addCertificationEntry"
                style="cursor: pointer"
              >
                <v-btn
                  icon
                  color="green"
                  style="background-color: transparent"
                  flat
                  tile
                  width="28"
                  height="28"
                >
                  <v-icon left color="white">mdi-plus</v-icon>
                </v-btn>
                <span class="ms-2 blue--text">
                  Tambah Sertifikasi/Lisensi
                </span>
              </div>
            </div>

            <div v-if="section.title === 'Penghargaan'">
              <div
                v-for="(award, index) in form.awards"
                :key="index"
                class="award-entry mb-4"
              >
                <v-card
                  outlined
                  class="form-field-card mt-2"
                  elevation="8"
                  style="border: 1px solid #1e88e5"
                >
                  <v-card-title class="d-flex align-center">
                    Penghargaan {{ index + 1 }}
                    <v-spacer></v-spacer>
                    <v-btn
                      icon
                      color="red"
                      style="background-color: transparent"
                      flat
                      tile
                      width="28"
                      height="28"
                      @click="removeAwardEntry(index)"
                    >
                      <v-icon>mdi-delete</v-icon>
                    </v-btn>
                  </v-card-title>

                  <v-card-text>
                    <v-row>
                      <v-col cols="12" md="6">
                        <v-text-field
                          v-model="award.name"
                          label="Nama Penghargaan"
                          outlined
                          required
                        ></v-text-field>
                      </v-col>
                      <v-col cols="12" md="6">
                        <v-text-field
                          v-model="award.issuer"
                          label="Pemberi Penghargaan"
                          outlined
                          required
                        ></v-text-field>
                      </v-col>
                    </v-row>

                    <v-row>
                      <v-col cols="12">
                        <v-autocomplete
                          v-model="award.year"
                          :items="years"
                          label="Tahun Penerimaan"
                          outlined
                          required
                        ></v-autocomplete>
                      </v-col>
                    </v-row>
                  </v-card-text>
                </v-card>
              </div>

              <div
                class="d-flex align-center"
                @click="addAwardEntry"
                style="cursor: pointer"
              >
                <v-btn
                  icon
                  color="green"
                  style="background-color: transparent"
                  flat
                  tile
                  width="28"
                  height="28"
                >
                  <v-icon left color="white">mdi-plus</v-icon>
                </v-btn>
                <span class="ms-2 blue--text"> Tambah Penghargaan </span>
              </div>
            </div>

            <div v-if="section.title === 'Skills'">
              <v-card
                outlined
                class="form-field-card mt-2"
                elevation="8"
                style="border: 1px solid #1e88e5"
              >
                <v-card-text>
                  <div class="d-flex align-center mb-3">
                    <v-icon color="blue" left>mdi-information-outline</v-icon>
                    <span class="ml-2 text-muted">
                      <strong>Hard skill</strong> adalah kemampuan yang dapat
                      diukur secara kuantitatif, seperti kemampuan bahasa
                      pemrograman, desain grafis, dll.<br />
                      <strong>Soft skill</strong> adalah kemampuan yang sulit
                      diukur secara kuantitatif, seperti kemampuan komunikasi,
                      kerja sama tim, dll.<br />
                      <strong>Software skill</strong> adalah kemampuan dalam
                      menggunakan software tertentu, seperti Microsoft Office,
                      Adobe Photoshop, dll.
                    </span>
                  </div>
                  <v-row>
                    <v-col cols="12" md="6">
                      <v-text-field
                        v-model="form.skills.hardSkills"
                        label="Hard Skill"
                        placeholder="Pisahkan dengan koma (,)"
                        outlined
                        required
                      ></v-text-field>
                    </v-col>
                    <v-col cols="12" md="6">
                      <v-text-field
                        v-model="form.skills.softSkills"
                        label="Soft Skill"
                        placeholder="Pisahkan dengan koma (,)"
                        outlined
                      ></v-text-field>
                    </v-col>
                  </v-row>
                  <v-row>
                    <v-col cols="12">
                      <v-text-field
                        v-model="form.skills.softwareSkills"
                        label="Software Skill"
                        placeholder="Pisahkan dengan koma (,)"
                        outlined
                        required
                      ></v-text-field>
                    </v-col>
                  </v-row>
                </v-card-text>
              </v-card>
            </div>
          </div>
        </v-card>

        <v-btn color="primary" block @click="submitForm" :loading="loading">Generate CV</v-btn>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import {
  getPositions,
  getPhrasesByPosition,
  getEducationalLevels,
  getFieldsByLevel,
  getPhrasesByField,
  updateDataCv,
  getCvById,
  generateCv
} from "@/services/api";

export default {
  name: "TambahPage",
  data() {
    return {
      expandedSection: null, // to track which section is expanded
      sections: [
        { title: "Objektif", icon: "mdi-target" },
        { title: "Informasi Pribadi", icon: "mdi-account" },
        { title: "Riwayat Pendidikan", icon: "mdi-school" },
        { title: "Riwayat Pekerjaan", icon: "mdi-briefcase" },
        { title: "Sertifikasi/Lisensi", icon: "mdi-certificate" },
        { title: "Penghargaan", icon: "mdi-trophy" },
        { title: "Skills", icon: "mdi-lightbulb" },
      ],
      educationLevels: [
        "SMA",
        "SMK",
        "Mas",
        "Sarjana",
        "Master",
        "Ph.D",
        "Diploma III",
        "Diploma IV",
        "Sertifikasi",
        "GCE O-Level",
        "GCE N-Level",
      ],
      form: {
        objective: "",
        personalInfo: {
          namaLengkap: "",
          email: "",
          nomorHp: "",
          linkedinUrl: "",
          portofolioUrl: "",
          alamat: "",
        },
        educationHistory: [],
        workExperience: [],
        certifications: [],
        awards: [],
        skills: [],
      },
      dialog: {
        rekomendasiFrasaPekerjaan: false,
        rekomendasiFrasaPekerjaan2: false,
        rekomendasiFrasaPendidikan: false,
      },
      loading: false,
      tahun: [],
      showNotification: false,
      pekerjaanForm: {
        data: [],
        position: null,
        phrases: [],
      },
      pendidikanForm: {
        data: [],
        level: null,
        field: null,
        phrases: [],
      },
      debounceTimer: null,
      autoSaveInterval: null,
      searchQuery: null,
      employeeStatuses: ["Penuh Waktu", "Paruh Waktu", "Kontrak", "Magang"],
      quillOptions: {
        theme: "bubble",
        modules: {
          toolbar: [
            [{ list: "ordered" }, { list: "bullet" }],
            ["bold", "italic", "underline"],
          ],
        },
      },
    };
  },
  created() {
    getCvById(this.$route.query.id)
      .catch(() => {
        this.$router.push("/");
      })
      .then((res) => {
        this.form = res;
      });
    this.tahun = Array.from({ length: 50 }, (_, i) => 2024 - i);
  },
  computed: {
    filteredJobs() {
      if (this.searchQuery === null) {
        return this.pekerjaanForm.data;
      }
      return this.pekerjaanForm.data.filter((job) =>
        job.toLowerCase().includes(this.searchQuery.toLowerCase())
      );
    },
    filteredPhrases() {
      if (this.searchQuery === null) {
        return this.pekerjaanForm.phrases;
      }
      return this.pekerjaanForm.phrases.filter((phrase) =>
        phrase.toLowerCase().includes(this.searchQuery.toLowerCase())
      );
    },
    filteredPhrasesPendidikan() {
      if (this.searchQuery === null) {
        return this.pendidikanForm.phrases;
      }
      return this.pendidikanForm.phrases.filter((phrase) =>
        phrase.toLowerCase().includes(this.searchQuery.toLowerCase())
      );
    },
  },
  watch: {
    form: {
      handler() {
        this.debounceSave();
      },
      deep: true,
    },
  },
  methods: {
    async toggleSection(index) {
      this.expandedSection = this.expandedSection === index ? null : index; // Toggle the section
      await new Promise((resolve) => setTimeout(resolve, 500));
      this.$nextTick(() => {
        if (this.$refs.objektif) {
          this.$refs.objektif[0].setHTML(this.form.objective);
        }
        this.form.workExperience.forEach((job, index) => {
          if (this.$refs["workExperienceDescription" + index]) {
            this.$refs["workExperienceDescription" + index][0].setHTML(
              job.description
            );
          }
        });
        this.form.educationHistory.forEach((education, index) => {
          if (this.$refs["educationDescription" + index]) {
            this.$refs["educationDescription" + index][0].setHTML(
              education.description
            );
          }
        });
      });
    },
    async openDialogRekomendasiFrasaPekerjaan() {
      this.dialog.rekomendasiFrasaPekerjaan = true;
      const positions = await getPositions();
      this.pekerjaanForm.data = positions;
    },

    closeDialogRekomendasiFrasaPekerjaan() {
      this.dialog.rekomendasiFrasaPekerjaan = false;
    },

    async openDialogRekomendasiFrasaPekerjaan2() {
      this.dialog.rekomendasiFrasaPekerjaan2 = true;
      const positions = await getPositions();
      this.pekerjaanForm.data = positions;
    },

    closeDialogRekomendasiFrasaPekerjaan2() {
      this.dialog.rekomendasiFrasaPekerjaan2 = false;
      this.pekerjaanForm.position = null;
      this.pekerjaanForm.phrases = [];
    },

    async openDialogRekomendasiFrasaPendidikan() {
      this.dialog.rekomendasiFrasaPendidikan = true;
      const levels = await getEducationalLevels();
      this.pendidikanForm.data = levels;
    },

    closeDialogRekomendasiFrasaPendidikan() {
      this.dialog.rekomendasiFrasaPendidikan = false;
    },

    async selectLevel(levelId) {
      this.pendidikanForm.level = levelId;
      const fields = await getFieldsByLevel(levelId);
      this.pendidikanForm.data = fields;
    },

    async selectField(fieldId) {
      this.pendidikanForm.field = fieldId;
      const phrases = await getPhrasesByField(
        this.pendidikanForm.level,
        fieldId
      );
      this.pendidikanForm.phrases = phrases;
    },

    async selectPosition(positionId) {
      this.pekerjaanForm.position = positionId;

      const phrases = await getPhrasesByPosition(positionId);
      this.pekerjaanForm.phrases = phrases;
    },

    selectPhrase(phrase) {
      this.$refs.objektif[0].setHTML(phrase + "\n");
      this.form.objective += phrase + "\n";
      this.dialog.rekomendasiFrasaPekerjaan = false;
    },

    selectPhrase2(phrase, index) {
      console.log(this.$refs["workExperienceDescription"]);
      this.$refs["workExperienceDescription" + index][0].setHTML(phrase);
      this.form.workExperience[index].description = phrase;
      this.dialog.rekomendasiFrasaPekerjaan2 = false;
    },

    selectPhrasePendidikan(phrase, index) {
      this.$refs["educationDescription" + index][0].setHTML(phrase + "\n");
      this.form.educationHistory[index].description += phrase + "\n";
      this.dialog.rekomendasiFrasaPendidikan = false;
    },

    async submitForm() {
      this.loading = true;
      try {
        const cvData = this.form;
        const response = await generateCv({
          cvData,
        });

        // Download file
        const link = document.createElement('a');
        link.href = response.path;
        link.download = 'CV.pdf'; 
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);

        this.$toast.success('CV berhasil di-generate!');
        this.loading = false;

        await new Promise((resolve) => setTimeout(resolve, 1000));
        this.$router.push("/");
      } catch (error) {
        this.$toast.error('Gagal men-generate CV. Silakan coba lagi.');
        console.error('Error generating CV:', error);
        this.loading = false;
      }
    },

    onEditorInput() {
      this.form.objective = this.$refs.objektif[0].getHTML();
    },

    onEducationDescriptionChange(index) {
      this.form.educationHistory[index].description =
        this.$refs["educationDescription" + index][0].getHTML();
    },

    onWorkExperienceDescriptionChange(index) {
      this.form.workExperience[index].description =
        this.$refs["workExperienceDescription" + index][0].getHTML();
    },

    async saveCvData() {
      try {
        // Call the API to save CV data
        await updateDataCv({
          id: this.$route.query.id,
          data: this.form,
        });
        this.showNotification = true;
      } catch (error) {
        console.error("Failed to auto-save CV:", error);
      }
    },
    startAutoSave() {
      this.autoSaveInterval = setInterval(() => {
        this.saveCvData();
      }, 10000); // Auto-save every 10 seconds
    },
    debounceSave() {
      if (this.debounceTimer) clearTimeout(this.debounceTimer);

      // Set a new timer to save after 10 seconds of inactivity
      this.debounceTimer = setTimeout(() => {
        this.saveCvData();
      }, 10000); // 10-second delay
    },

    addEducationEntry() {
      this.form.educationHistory.push({
        institution: "",
        location: "",
        startYear: "",
        endYear: "",
        educationLevel: "",
        program: "",
        gpa: "",
        maxGpa: "",
        description: "",
        currentlyStudying: false,
      });
    },
    removeEducationEntry(index) {
      this.form.educationHistory.splice(index, 1);
    },

    addJobEntry() {
      this.form.workExperience.push({
        institution: "",
        position: "",
        employeeStatus: "",
        startDate: "",
        endDate: "",
        location: "",
        description: "",
        currentlyWorking: false,
        startDateMenu: false,
        endDateMenu: false,
      });
    },
    removeJobEntry(index) {
      this.form.workExperience.splice(index, 1);
    },

    addCertificationEntry() {
      this.form.certifications.push({
        name: "",
        issuer: "",
        number: "",
        year: "",
      });
    },
    removeCertificationEntry(index) {
      this.form.certifications.splice(index, 1);
    },

    addAwardEntry() {
      this.form.awards.push({
        name: "",
        issuer: "",
        year: "",
      });
    },
    removeAwardEntry(index) {
      this.form.awards.splice(index, 1);
    },
  },
};
</script>














<style scoped>
/* Center the entire container */
.centered-container {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 100vh; /* Center vertically */
}

/* Custom card styling */
.custom-card {
  border-radius: 10px;
  overflow: hidden;
  transition: box-shadow 0.3s;
  min-height: 70px;
  background-color: #f5faff;
  border: 1px solid #1e88e5;
}

.custom-card.expanded-card {
  border-color: #1565c0;
}

.custom-card:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

/* Card Header styling */
.card-header {
  display: flex;
  align-items: center;
  padding: 12px 16px;
  font-weight: 500;
  cursor: pointer;
}

.card-header .header-title {
  font-weight: 600;
  font-size: 16px;
  color: #1e88e5;
}

.card-header .header-icon {
  margin-right: 8px;
}

.card-header .v-btn {
  margin-left: auto;
}

/* Content styling */
.card-content {
  padding: 16px;
  font-size: 14px;
  color: #333;
  background-color: white;
}

.info-icon {
  font-size: 20px;
  margin-bottom: -4px;
}

.info-text {
  color: #666;
  font-size: 14px;
  margin-top: 8px;
  margin-bottom: 16px;
}

.description-textarea {
  width: 100%;
  margin-top: 12px;
  margin-bottom: 8px;
}

.quill-editor-container {
  position: relative;
  width: 100%;
}

.rekomendasi-frasa {
  position: absolute;
  right: 20px;
  top: -5px;
  padding: 8px;
  border-radius: 5px;
  font-size: 14px;
  color: #333;
  z-index: 10; /* Ensure it is above the editor */
}

.rekomendasi-frasa p {
  margin: 0;
  padding: 0;
}

.vue-quill {
  max-width: 800px;
  margin: 0 auto;
  height: 800px;
}

.floating-card {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  z-index: 1000;
}

.floating-card-pendidikan {
  position: absolute;
  top: 75%;
  left: 50%;
  transform: translate(-50%, -50%);
  z-index: 1000;
}

.phrase-item {
  cursor: pointer;
}

.job-item {
  cursor: pointer;
}

.rounded-field {
  border-radius: 12px;
  padding: 10px;
}

.v-text-field,
.v-textarea {
  border-radius: 8px !important;
}

.mb-3 {
  margin-bottom: 12px;
}
</style>
