<template>
  <div class="home">
    <hr id="home_hr" />
    <div class="home_stocks_container">
      <Stock
        v-for="(stock, index) in stocks"
        :key="index"
        v-bind:ticker="stock.ticker"
        v-bind:price="stock.price"
        v-bind:change="stock.change"
      ></Stock>
    </div>
    <hr id="home_hr" />
    <div class="home_article">
      <!--
      <div class="article_image_container">
        <img
          src="https://finance.univie.ac.at/fileadmin/_processed_/csm_web_Banking-and-Finance_Hauptbi_672df5bcac.jpg"
          alt="Globe"
          class="home_article_image"
        />
      </div>
    -->
      <div class="home_article_text_container">
        <h2 class="home_article_title">
          <font color="#9de0bb">Finance Boi</font>, A New Way to Optimize Your
          Portfolio
        </h2>
        <p class="home_article_info">
          Our focus is to use
          <a href="https://azure.microsoft.com/en-us/overview/ai-platform/"
            ><font color="lightblue">Azure AI's</font></a
          >
          Cognitive Services on financial news articles combined with portfolio
          optimization algorithms in order to create the best portfolio for your
          account. Currently only supports stocks from the NASDAQ 100.
        </p>
      </div>
    </div>
    <div class="home_bottom_section">
      <div class="home_articles_container">
        <h2 v-if="loading">Loading news articles...</h2>
        <Article
          v-for="(article, index) in news"
          :key="index"
          v-bind:title="article.title"
          v-bind:description="article.description"
          v-bind:ticker="article.Ticker"
          v-bind:article_link="article.link"
          v-bind:sentiment="article.sentiment"
          v-bind:change="article.change"
        ></Article>
      </div>
      <div class="home_watchlist_container" v-if="user">
        <h2 class="home_watchlist_title">Watch List</h2>
        <WatchItem
          v-for="(watchitem, index) in watchitemData"
          :key="index"
          v-bind:ticker="watchitemData[index].ticker"
          v-bind:price="watchitemData[index].close"
          v-bind:change="watchitemData[index].change"
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
import StocksAPI from "@/services/StocksAPI.js";
import UserAPI from "@/services/UserAPI.js";
import firebase from "firebase";

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
      user: null,
      loading: true,
      stocks: [
        { ticker: "GOOG", price: "1111", change: "+5%" },
        { ticker: "MSFT", price: "420", change: "+6%" },
        { ticker: "AMZN", price: "5555", change: "+10%" },
        { ticker: "TSLA", price: "5555", change: "+10%" },
        { ticker: "FB", price: "4455", change: "+40%" },
        { ticker: "NVDA", price: "1337", change: "+69%" },
        { ticker: "NFLX", price: "1234", change: "+44%" }
      ],
      watchitems: [],
      watchitemData: [],
      news: []
    };
  },
  mounted() {
    this.loadNews();
    this.getUser();
    this.getWatchlist();
  },
  methods: {
    async loadNews() {
      const response = await NewsAPI.getNews();
      this.news = response.data;
      this.loading = false;
    },
    async getWatchlist() {
      const watchitems = await UserAPI.getWatchlist(this.user);
      for (var i = 0; i < watchitems.data[0].stocks.length; i++) {
        this.watchitems.push(watchitems.data[0].stocks[i]);
      }
      for (var item in this.watchitems) {
        const response = await StocksAPI.getStock(this.watchitems[item].ticker);
        response.data[0].close = String(response.data[0].close).slice(0, 8);
        response.data[0].change = String(response.data[0].change).slice(0, 8);
        this.watchitemData.push(response.data[0]);
      }
    },
    getUser() {
      var user = firebase.auth().currentUser;
      this.user = user.email;
    }
  }
};
</script>

<style>
button {
  margin-bottom: 15px;
  width: 8%;
  cursor: pointer;
}
</style>
