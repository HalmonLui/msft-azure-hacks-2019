<template>
  <div class="register">
    <h3>Registration Page</h3>
    <input type="text" v-model="email" placeholder="Email"><br>
    <input type="password" v-model="password" placeholder="Password"><br>
    <button @click="register">Sign Up</button>
    <span>Or go back to <router-link to="/login">Login</router-link></span>
  </div>
</template>

<script>
  import firebase from 'firebase';

  export default {
    name: 'register',
    data() {
      return {
        email: '',
        password:''
      }
    },
    methods: {
      register: function() {
        firebase.auth().createUserWithEmailAndPassword(this.email, this.password).then(
          (user) => {
            this.$router.replace('/')
          },
          (err) => {
            alert(err.message)
          }
        );
      }
    }
  }
</script>

<style scoped>
  .register {
    margin-top: 100px;
  }
  input {
    margin: 10px 0;
    width: 20%;
    padding: 10px;
  }
  button {
    margin-top: 10px;
    width: 15%;
    cursor: pointer;
  }
  span {
    display: block;
    margin-top: 20px;
    margin-bottom: 20px;
    font-size: 13px;
    cursor: pointer;
  }
</style>
