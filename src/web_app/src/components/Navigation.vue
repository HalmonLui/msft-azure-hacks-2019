<template>
  <div id="navbar">
    <div>
      <router-link class="navbar_link" id="navbar_logo" to="/"
        ><img src="../assets/images/logo.png" alt="Finance Boi Logo"
      /></router-link>
    </div>
    <div id="navbar_links_container">
      <nav id="navbar_links">
        <router-link
          class="navbar_link"
          v-for="routes in links"
          v-bind:key="routes.id"
          :to="`${routes.page}`"
          >{{ routes.text }}</router-link
        >
        <router-link class="navbar_link" to="/login">LOGIN</router-link>
        <router-link class="navbar_link" id="navbar_register" to="/register"
          >Register</router-link
        >
      </nav>
    </div>
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
          text: "HOME",
          page: "/"
        },
        {
          id: 1,
          text: "NEWS",
          page: "/News"
        },
        {
          id: 2,
          text: "STOCKS",
          page: "/Stocks"
        }
      ]
    };
  }
};
</script>
<style></style>
