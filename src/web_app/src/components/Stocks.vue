<template>
  <div class="stocks">
    <hr id="home_hr" />
    <div>
      <p>Search: Bing Search Boi In Here</p>
    </div>
    <hr id="home_hr" />
    <div class="stocks_body">
      <div class="stocks_stockslist_container">
        <div class="stocklist" id="stocklist_title">
          <div class="stockowned_image_container">
            <img class="stockowned_image" />
          </div>
          <div class="stocks_stocks_title">
            <h4>COMPANY</h4>
            <h4>PRICE</h4>
            <h4>CHANGE</h4>
          </div>
        </div>
        <h1 class="home_watchlist_title" v-if="loading">
          Loading stock data...
        </h1>
        <Stocklist
          v-for="(stock, index) in stocks"
          :key="index"
          v-bind:ticker="stockData[index].ticker"
          v-bind:price="stockData[index].close"
          v-bind:change="stockData[index].change"
          @click.native="pickStock(index)"
        ></Stocklist>
      </div>
      <div class="stocks_watchlist_container">
        <h2 class="home_watchlist_title">Watch List</h2>
        <WatchItem
          v-for="(watchitem, index) in watchitems"
          :key="index"
          v-bind:ticker="watchitems[index].ticker"
          v-bind:price="watchitems[index].ticker"
          v-bind:change="watchitems[index].ticker"
        ></WatchItem>
      </div>
    </div>
  </div>
</template>

<script>
import Stocklist from "./subcomponents/Stocklist";
import WatchItem from "./subcomponents/WatchItem";
import StocksAPI from "@/services/StocksAPI.js";
import UserAPI from "@/services/UserAPI.js";
import firebase from "firebase";
export default {
  name: "Stocks", //this is the name of the component
  components: {
    Stocklist: Stocklist,
    WatchItem: WatchItem
  },
  data() {
    return {
      user: null,
      loading: true,
      stocks: [],
      stockData: [],
      watchitems: []
    };
  },
  mounted() {
    this.loadStocks();
    this.getUser();
    this.getWatchlist();
  },
  methods: {
    async loadStocks() {
      const loadedstocks = await StocksAPI.getStocks();
      this.loading = false;
      this.stocks = loadedstocks.data;
      for (var item in this.stocks) {
        const response = await StocksAPI.getStock(this.stocks[item].ticker);
        response.data[0].close = String(response.data[0].close).slice(0, 8);
        response.data[0].change = String(response.data[0].change).slice(0, 8);
        this.stockData.push(response.data[0]);
      }
    },
    async pickStock(index) {
      if (this.watchitems.length <= 15) {
        for (var item in this.watchitems) {
          if (this.stockData[index].ticker == this.watchitems[item].ticker) {
            alert("You already got this one sonny");
            return;
          }
        }
        const response = await UserAPI.addStock(
          this.user,
          this.stockData[index].ticker
        );
        this.watchitems.push(this.stockData[index]);
      } else {
        alert("Chilllll don't buy over 15 stocks");
      }
    },
    async getWatchlist() {
      const watchitems = await UserAPI.getWatchlist(this.user);
      for (var i = 0; i < watchitems.data[0].stocks.length; i++) {
        this.watchitems.push(watchitems.data[0].stocks[i]);
      }
    },
    getUser() {
      var user = firebase.auth().currentUser;
      this.user = user.email;
    }
  }
};
</script>
<style></style>
