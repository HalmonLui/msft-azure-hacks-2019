<template>
  <div class="home">
    <hr id="home_hr" />
    <div class="home_stocks_container">
      <Stock
        v-for="stock in stocks"
        v-bind:symbol="stock.symbol"
        v-bind:price="stock.price"
        v-bind:change="stock.change"
      ></Stock>
    </div>
    <hr id="home_hr" />
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
      <Article
        v-for="article in articles"
        v-bind:title="article.title"
        v-bind:text="article.text"
        v-bind:article_image="article.article_image"
      ></Article>
    </div>
    <h1>{{ msg }}</h1>
  </div>
</template>

<script>
import Article from "./subcomponents/Article";
import Stock from "./subcomponents/Stock";
export default {
  name: "Home",
  components: {
    Article: Article,
    Stock: Stock
  },
  data() {
    return {
      msg: "Welcome to Finance Boi",
      stocks: [
        { symbol: "GOOG", price: "1111", change: "+5%" },
        { symbol: "MSFT", price: "420", change: "+6%" },
        { symbol: "AMZN", price: "5555", change: "+10%" },
        { symbol: "TSLA", price: "5555", change: "+10%" },
        { symbol: "KEVT", price: "4455", change: "+40%" },
        { symbol: "SNAM", price: "1337", change: "+69%" },
        { symbol: "BRHE", price: "1234", change: "+44%" }
      ],
      articles: [
        {
          title: "Stonks are on the rise",
          text:
            "There are tons of info on stonks. For more checkout r/wallstreetbets"
        },
        {
          title: "Stonks are on the rise",
          text:
            "There are tons of info on stonks. For more checkout r/wallstreetbets"
        },
        {
          title: "Stonks are on the rise",
          text:
            "There are tons of info on stonks. For more checkout r/wallstreetbets"
        },
        {
          title: "Stonks are on the rise",
          text:
            "There are tons of info on stonks. For more checkout r/wallstreetbets"
        }
      ]
    };
  }
};
</script>

<style></style>
