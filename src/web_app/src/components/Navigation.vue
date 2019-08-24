<template>
  <div>
    <h2>Nav Bar</h2>
    <nav>
      <router-link
        class="spacing"
        v-for="routes in links"
        v-bind:key="routes.id"
        :to="`${routes.page}`"
        >{{ routes.text }}</router-link
      >
      <router-link to="/login">Login</router-link>
      <router-link to="/register">Register</router-link>
    </nav>
  </div>
</template>

<script>
export default {
  name: "Navigation",
  data() {
    return {
      links: [
        {
          id: 0,
          text: "Home",
          page: "/"
        },
        {
          id: 1,
          text: "News",
          page: "/News"
        },
        {
          id: 2,
          text: "Stocks",
          page: "/Stocks"
        }
      ]
    };
  }
};
</script>
<style>
.spacing {
  margin-right: 10px;
}
</style>
