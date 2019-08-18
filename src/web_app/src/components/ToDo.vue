<template lang="html">
  <div>
    <ul>
      <li v-for="todo in todos">
        <span>{{ todo }}</span>
      </li>
    </ul>
  </div>
</template>
<script>
import ToDoAPI from "@/services/ToDoAPI.js";
export default {
  data() {
    return {
      todos: []
    };
  },
  mounted() {
    this.loadTodos();
  },
  methods: {
    async loadTodos() {
      const response = await ToDoAPI.getToDos();
      this.todos = response.data;
    }
  }
};
</script>
<style lang="css"></style>
