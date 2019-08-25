<template>
  <div class="home">
    <hr id="home_hr" />
    <div class="home_stocks_container">
      <p>Subcomponent C Goes Here</p>
    </div>
    <hr id="home_hr" />
    <h1>{{ msg }}</h1>
    <h2>INSERT TITLE HERE BIG ARTICLE BOI GOES HERE</h2>
    <div class="home_articles_container">
      <Article></Article>
      <Article></Article>
      <Article></Article>
      <Article></Article>
    </div>
  </div>
</template>

<script>
import Article from "./subcomponents/Article";
export default {
  name: "Home",
  components: {
    Article: Article
  },
  data() {
    return {
      msg: "Welcome to Finance Boi"
    };
  }
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h1,
h2 {
  font-weight: normal;
}
ul {
  list-style-type: none;
  padding: 0;
}
li {
  display: inline-block;
  margin: 0 10px;
}
a {
  color: #42b983;
}
</style>
