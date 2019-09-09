<template>
  <div>
    <h1>Join Finance Boi</h1>
    <p>Already have an account? <a href="http://localhost:11964/?#/login">Login</a> </p>
  <form>
    First name:<br>
    <input type="text" name="firstname"><br><br>
    Last name:<br>
    <input type="text" name="lastname"><br><br>
    Email:<br>
    <input type="text" name="email"><br><br>
    Password:<br>
    <input type="password" name="password"><br><br>
  </form>
  <br>
  <input type="submit" value="Create Account">
  </div>
</template>

<script>
export default {
  name: 'Register',
  data(){
    return {
      email: "emailboi",
      web: "websiteboi"
    }
  }
}
</script>

<style scoped>
input, textarea {
  outline: none;
}

</style>
