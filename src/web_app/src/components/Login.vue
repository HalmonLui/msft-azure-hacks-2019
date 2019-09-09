<template>
  <div class="login">
    <h3>Sign In </h3>
    <input type="text" v-model="email" placeholder="Email"><br>
    <input type="password" v-model="password" placeholder="Password"><br>
    <button @click="login">Login</button>
    <p>Don't have an account? Register <router-link to="/register">here</router-link></p>
  </div>
</template>

<script>
  import firebase from 'firebase';

  export default {
    name: 'login',
    data() {
      return {
        email: '',
        password: ''
      };
    },
    methods: {
      login: function(){
        firebase.auth().signInWithEmailAndPassword(this.email, this.password).then(
          (user) => {
            this.$router.replace('/')
            alert('Success')
          },
          (err) => {
            alert(err.message)
          }
        )
      }
    }
  }
</script>

<style scoped>
  .login {
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
  p {
    margin-top: 30px;
    font-size: 13px;
  }
  p a {
    text-decoration: underline;
    cursor: pointer;
  }
</style>
