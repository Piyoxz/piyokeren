import FieldContainer from "@/components/Field/FieldContainer.vue";

export default {
  name: "DatePickerField",
  props: {
    value: String,
    type: {
      type: String,
      default: "date",
    },
    placeholder: String,
    height: String | Number,
    dense: {
      type: Boolean,
      default: true,
    },
    label: String,
    errorMessages: Array,
    rules: Array,
    required: {
      type: Boolean,
      default: false,
    },
    readonly: {
      type: Boolean,
      default: false,
    },
    disabled: {
      type: Boolean,
      default: false,
    },
    md: {
      type: String | Number,
      default: 5,
    },
  },
  mounted() {
    this.$watch(
      () => {
        return {
          hasInput: this.$refs.textField.hasInput,
          hasError: this.$refs.textField.hasError,
        };
      },
      (val) => {
        if (val.hasInput) {
          this.error = val.hasError;
        }
      }
    );
  },
  components: {
    FieldContainer,
  },
  data() {
    return {
      display: false,
      error: false,
    };
  },
  computed: {
    vMenu() {
      return {
        closeOnContentClick: false,
        transition: "scale-transition",
        offsetY: true,
        nudgeLeft: 10,
        nudgeBottom: 5,
        maxWidth: 290,
        minWidth: 290,
      };
    },
    vTextField() {
      return {
        value: this.value ? this.dateFormat(this.value) : null,
        dense: this.dense,
        height: this.height,
        placeholder: this.placeholder,
        outlined: true,
        readonly: true,
        clearable: !this.readonly,
        appendIcon: "icon-date",
        backgroundColor: this.disabled ? "grey lighten-3" : "white",
        hideDetails: "auto",
        errorMessages: this.errorMessages,
        rules: this.validationRules,
        required: this.required,
        disabled: this.disabled,
      };
    },
    vDatePicker() {
      return {
        locale: "id",
        noTitle: true,
        type: this.type,
      };
    },
    validationRules() {
      let rules = this.rules ? [...this.rules] : [];

      if (this.required) {
        rules = [
          ...rules,
          (v) =>
            !!v ||
            (this.label ? this.label + " harus diisi." : "must be filled"),
        ];
      }

      return rules;
    },
    parsePattern() {
      switch (this.type) {
        case "date":
          return "YYYY-MM-DD";
        case "month":
          return "YYYY-MM";
      }
    },
    formatPattern() {
      switch (this.type) {
        case "date":
          return "DD MMM YYYY";
        case "month":
          return "MMM YYYY";
      }
    },
  },
  methods: {
    dateSelected($event) {
      this.$emit("input", $event);
      this.display = false;
    },
    dateParse(value) {
      return this.$options.filters.dateParse(value, this.parsePattern);
    },
    dateFormat(value) {
      return this.$options.filters.dateFormat(
        this.dateParse(value),
        this.formatPattern
      );
    },
    clear() {
      this.$emit("input", null);
    },
    input($event) {
      if (!$event) {
        this.$emit("input", null);
      }
    },
    blur($event) {
      if (this.$refs.textField) {
        this.error = this.$refs.textField.hasError;
      }
      this.$emit("blur", $event);
    },
  },
  watch: {
    value(value) {
      console.log("change value", value);
    },
  },
};
