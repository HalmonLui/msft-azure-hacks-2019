<template>
  <div class="register">
    <img src="../assets/images/register.png" class="register_image" />
    <div class="register_form_container">
      <h2 class="register_title">Join Finance Boi!</h2>
      <p class="register_text">
        Already have an account? <router-link to="/login">Login</router-link>
      </p>
      <div class="register_name_container">
        <input
          class="register_form"
          id="register_form_name"
          type="text"
          v-model="firstname"
          placeholder="First Name"
        />
        <input
          class="register_form"
          id="register_form_name"
          type="text"
          v-model="lastname"
          placeholder="Last Name"
        />
      </div>
      <input
        class="register_form"
        type="text"
        v-model="email"
        placeholder="Email"
      />
      <input
        class="register_form"
        type="password"
        v-model="password"
        placeholder="Password"
      />
      <input
        class="register_form"
        type="password"
        v-model="confirmpassword"
        placeholder="Confirm Password"
      />
      <button class="register_button" @click="registerWithFirebase">
        Create Account
      </button>
    </div>
  </div>
</template>

<script>
import firebase from "firebase";

export default {
  name: "register",
  data() {
    return {
      email: "",
      password: ""
    };
  },
  methods: {
    register: function() {
      if (this.password == this.confirmpassword) {
        this.$store.dispatch("signUpAction", user).then(
          user => {
            this.$router.replace("/");
          },
          err => {
            alert(err.message);
          }
        );
      } else {
        alert("Please confirm your password");
      }
    }
  }
};
</script>

<style scoped>
.register {
  margin-top: 15%;
  display: flex;
  margin-bottom: 15%;
}
.register_image {
  flex: 0.7;
  margin: 5%;
}
.register_form_container {
  flex: 1;
  display: flex;
  flex-direction: column;
  text-align: center;
  align-items: center;
}
.register_title {
  font-size: 30px;
}
.register_text {
  color: gray;
  font-size: 1em;
}
.register_name_container {
  display: flex;
  flex-direction: row;
  width: 88%;
  height: 100%;
}
#register_form_name {
  padding: 2.4%;
}
.register_form {
  padding: 2%;
  width: 80%;
  margin: 2%;
  border-radius: 2px;
  border: 1px solid lightgray;
}
.register_button {
  background-color: #50d282;
  border: none;
  border-radius: 2px;
  color: white;
  width: 85%;
  padding: 2.5%;
  margin: 2%;
}
.register_button:hover {
  background-color: white;
  color: #50d282;
  cursor: pointer;
  border: 0.5px solid #50d282;
}
</style>
