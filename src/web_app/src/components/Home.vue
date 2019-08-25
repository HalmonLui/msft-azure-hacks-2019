<template>
  <div class="home">
    <hr id="home_hr" />
    <div class="home_stocks_container">
      <p>Subcomponent C Goes Here</p>
    </div>
    <hr id="home_hr" />
    <h1>{{ msg }}</h1>
    <a class="home_article" href="https://www.google.com">
      <div class="article_image_container">
        <img
          src="https://i.ytimg.com/vi/if-2M3K1tqk/maxresdefault.jpg"
          alt="Finance Boi Logo"
          class="article_image"
        />
      </div>
      <div class="article_text_container">
        <h2 class="article_title">Stonks are on the rise</h2>
        <p class="article_info">
          There are tons of info on stonks. For more checkout r/wallstreetbets
        </p>
      </div>
    </a>
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
