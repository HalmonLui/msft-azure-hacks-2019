<template>
  <div class="profile">
    <hr id="home_hr" class="profile_hr" />
    <div>
      <h1>Profile</h1>
      <p>Hello {{ user }}</p>
      <p>PERSONALIZATION PROFILE PAGE COMING SOON...</p>
    </div>
  </div>
</template>

<script>
import firebase from "firebase";
export default {
  name: "Profile", //this is the name of the component
  components: {},
  data() {
    return {
      msg: "Welcome to Finance Boi",
      user: null
    };
  },
  mounted() {
    this.getUser();
  },
  methods: {
    getUser() {
      var user = firebase.auth().currentUser;
      this.user = user.email;
    }
  }
};
</script>
<style scoped>
.profile {
  margin-top: 8%;
}
</style>
