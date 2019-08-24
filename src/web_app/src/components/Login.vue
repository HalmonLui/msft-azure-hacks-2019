<template>
  <div>
    <h1>Login</h1>
  <p>
    <ul>
      <li>Email: {{email}}</li>
      <li>Website: {{web}}</li>
    </ul>
  </p>
  </div>
</template>

<script>
export default {
  name: 'Login',
  data(){
    return {
      email: "emailboi",
      web: "websiteboi"
    }
  }
}
</script>
