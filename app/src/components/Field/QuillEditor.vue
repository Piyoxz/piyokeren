<template>
  <div ref="editorContainer" class="quill-editor-container"></div>
</template>

<script>
import Quill from 'quill';

export default {
  name: 'QuillEditor',
  props: {
    value: {
      type: String,
      default: ''
    }
  },
  mounted() {
    this.initQuill();
  },
  methods: {
    initQuill() {
      this.quill = new Quill(this.$refs.editorContainer, {
        theme: 'snow',
        modules: {
          toolbar: [
            [{ 'header': '1' }, { 'header': '2' }],
            [{ 'list': 'ordered' }, { 'list': 'bullet' }],
            ['bold', 'italic', 'underline'],
            [{ 'align': [] }],
            ['link'],
            ['clean']
          ],
        },
      });

      // Set initial content from `value` prop
      this.quill.root.innerHTML = this.value;

      // Listen for changes to update the `value`
      this.quill.on('text-change', () => {
        this.$emit('input', this.quill.root.innerHTML); // Emit the input event to the parent component
      });
    }
  },
};
</script>

<style scoped>
.quill-editor-container {
  height: 300px;  /* Increased height for the Quill editor */
  border: 1px solid #ccc;
  border-radius: 4px;
  margin-top: 20px;
}
</style>
