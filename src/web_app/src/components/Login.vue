<template>
  <div class="login">
    <div class="login_form_container">
      <h2 class="login_title">Sign In</h2>
      <input
        class="login_form"
        type="text"
        v-model="email"
        placeholder="Email"
      /><br />
      <input
        class="login_form"
        type="password"
        v-model="password"
        placeholder="Password"
      /><br />
      <button class="login_button" @click="loginWithFirebase">Login</button>
      <p class="login_text">
        Don't have an account? Register
        <router-link to="/register">here</router-link>
      </p>
    </div>
  </div>
</template>

<script>
import firebase from "firebase";

export default {
  name: "login",
  data() {
    return {
      email: "",
      password: ""
    };
  },
  methods: {
    login: function() {
      firebase
        .auth()
        .signInWithEmailAndPassword(this.email, this.password)
        .then(
          user => {
            this.$router.replace("/");
            alert("Success");
          },
          err => {
            alert(err.message);
          }
        );
    },
    loginWithFirebase() {
      const user = {
        email: this.email,
        password: this.password
      };
      this.$store.dispatch("signInAction", user).then(
        user => {
          this.$router.replace("/portfolio");
        },
        err => {
          alert(err.message);
        }
      );
    }
  }
};
</script>

<style scoped>
.login {
  height: 50vh;
  margin-top: 15%;
  margin-bottom: 15%;
}
.login_form_container {
  display: flex;
  flex-direction: column;
  margin: auto;
  justify-content: center;
  align-items: center;
}
.login_title {
  font-size: 30px;
}
.login_text {
  color: gray;
  font-size: 1em;
}
.login_form {
  padding: 1%;
  width: 30%;
  margin: auto;
  border-radius: 2px;
  border: 1px solid lightgray;
}
.login_button {
  background-color: #50d282;
  border: none;
  border-radius: 2px;
  color: white;
  width: 32%;
  padding: 1.5%;
  margin: 1%;
}
.login_button:hover {
  background-color: white;
  color: #50d282;
  cursor: pointer;
  border: 0.5px solid #50d282;
}
</style>
