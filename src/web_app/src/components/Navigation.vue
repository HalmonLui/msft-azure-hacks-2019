<template>
  <div id="navbar">
    <div>
      <router-link class="navbar_link" id="navbar_logo" to="/"
        ><img
          class="navbar_image"
          src="../assets/images/logo.png"
          alt="Finance Boi Logo"
          title="Finance Boi"
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
        <div class="navbar_login" v-if="!userLoggedIn">
          <router-link class="navbar_link" to="/login">LOGIN</router-link>

          <router-link class="navbar_link" id="navbar_register" to="/register"
            >Register</router-link
          >
        </div>
        <div class="navbar_login" v-else>
          <router-link class="navbar_link" to="/profile">PROFILE</router-link>
          <button class="navbar_button" @click="logoutFromFirebase">
            Logout
          </button>
        </div>
      </nav>
    </div>
  </div>
</template>

<script>
import firebase from "firebase";
export default {
  name: "Navigation",
  computed: {
    userLoggedIn() {
      return this.$store.getters.user;
    }
  },
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
          text: "PORTFOLIO",
          page: "/Portfolio"
        },
        {
          id: 2,
          text: "STOCKS",
          page: "/Stocks"
        }
      ]
    };
  },
  mounted() {
    this.getUser();
  },
  methods: {
    logout: function() {
      firebase
        .auth()
        .signOut()
        .then(() => {
          this.$router.replace("login");
        });
    },
    getUser() {
      var user = firebase.auth().currentUser;
      this.user = user.email;
    },
    logoutFromFirebase() {
      this.$store.dispatch("signOutAction");
    }
  }
};
</script>
<style></style>
