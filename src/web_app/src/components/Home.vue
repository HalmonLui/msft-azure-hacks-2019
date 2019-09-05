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
          src="https://finance.univie.ac.at/fileadmin/_processed_/csm_web_Banking-and-Finance_Hauptbi_672df5bcac.jpg"
          alt="Globe"
          class="article_image"
        />
      </div>
      <div class="article_text_container">
        <h2 class="home_article_title">
          Finance Boi, A New Way to Optimize Your Portfolio
        </h2>
        <p class="home_article_info">
          Our focus is to use sentiment analysis on financial news articles
          combined with portfolio optimization algorithms in order to create the
          best portfolio for your account.
        </p>
      </div>
    </a>
    <div class="home_bottom_section">
      <div class="home_articles_container">
        <Article
          v-for="article in news"
          v-bind:title="article.title"
          v-bind:description="article.description"
          v-bind:article_image="
            '../../assets/images/logos/' + article.Ticker + '.png'
          "
          v-bind:ticker="article.Ticker"
          v-bind:article_link="article.link"
        ></Article>
      </div>
      <div class="home_watchlist_container">
        <h2 class="home_watchlist_title">Watch List</h2>
        <WatchItem
          v-for="watchitem in watchitems"
          v-bind:symbol="watchitem.symbol"
          v-bind:price="watchitem.price"
          v-bind:change="watchitem.change"
        ></WatchItem>
      </div>
    </div>
  </div>
</template>

<script>
import Article from "./subcomponents/Article";
import Stock from "./subcomponents/Stock";
import WatchItem from "./subcomponents/WatchItem";
import NewsAPI from "@/services/NewsAPI.js";
export default {
  name: "Home",
  components: {
    Article: Article,
    Stock: Stock,
    WatchItem: WatchItem
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
      watchitems: [
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
        }
      ],
      news: []
    };
  },
  mounted() {
    this.loadNews();
  },
  methods: {
    async loadNews() {
      const response = await NewsAPI.getNews();
      this.news = response.data;
    }
  }
};
</script>

<style></style>
