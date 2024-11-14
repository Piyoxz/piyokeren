<template>
  <FieldContainer :label="label" :md="md">
    <template #label>
      <!-- @slot Label field -->
      <slot
        name="label"
        v-bind="{ label, required, error: error || !!errorMessages }"
      >
        <div class="mt-2">
          <label :class="{ 'error--text': error || !!errorMessages }">{{
            label
          }}</label>
          <v-tooltip v-if="required" right>
            <template #activator="{ on }">
              <v-btn icon x-small color="red" v-on="on">
                <v-icon x-small> icon-search </v-icon>
              </v-btn>
            </template>
            <span>Wajib diisi.</span>
          </v-tooltip>
        </div>
      </slot>
    </template>

    <v-menu v-model="display" v-bind="vMenu">
      <template #activator="{ on }">
        <v-text-field
          v-if="!readonly || !disabled"
          ref="textField"
          v-bind="vTextField"
          style="
            border-radius: 0px;
            leter-spacing: 0.025rem;
            font-size: 0.75rem;
          "
          v-on="on"
          @click:append="display = !display"
          @update:error="(e) => (error = e)"
          @click:clear="clear()"
          @input="input($event)"
          @blur="blur($event)"
        />
        <v-text-field
          v-else
          v-bind="vTextField"
          style="border-radius: 0px"
          @update:error="(e) => (error = e)"
          @input="input($event)"
        />
      </template>

      <v-date-picker
        :key="value ? value : Math.random().toString(36).substring(7)"
        v-bind="vDatePicker"
        @input="dateSelected"
      />
    </v-menu>
  </FieldContainer>
</template>

<script src="./js/DatePickerField.js"></script>
