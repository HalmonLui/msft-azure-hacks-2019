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
        <Stocklist
          v-for="(stock, index) in stocks"
          :key="index"
          v-bind:ticker="stockData[index].ticker"
          v-bind:price="stockData[index].close"
          v-bind:change="stockData[index].change"
        ></Stocklist>
      </div>
      <div class="stocks_watchlist_container">
        <h2 class="home_watchlist_title">Watch List</h2>
        <WatchItem
          v-for="(watchitem, index) in watchitems"
          :key="index"
          v-bind:ticker="watchitem.ticker"
          v-bind:price="watchitem.price"
          v-bind:change="watchitem.change"
        ></WatchItem>
      </div>
    </div>
  </div>
</template>

<script>
import Stocklist from "./subcomponents/Stocklist";
import WatchItem from "./subcomponents/WatchItem";
import StocksAPI from "@/services/StocksAPI.js";
export default {
  name: "Stocks", //this is the name of the component
  components: {
    Stocklist: Stocklist,
    WatchItem: WatchItem
  },
  data() {
    return {
      stocks: [],
      stockData: [],
      watchitems: [
        { ticker: "GOOG", price: "1111", change: "+5%" },
        { ticker: "MSFT", price: "420", change: "+6%" },
        { ticker: "AMZN", price: "5555", change: "+10%" },
        { ticker: "TSLA", price: "5555", change: "+10%" },
        { ticker: "GOOG", price: "4455", change: "+40%" },
        { ticker: "GOOGL", price: "1337", change: "+69%" },
        { ticker: "AAPL", price: "1234", change: "+44%" }
      ]
    };
  },
  mounted() {
    this.loadStocks();
  },
  methods: {
    async loadStocks() {
      const loadedstocks = await StocksAPI.getStocks();
      this.stocks = loadedstocks.data;
      for (var item in this.stocks) {
        const response = await StocksAPI.getStock(this.stocks[item].ticker);
        response.data[0].close = String(response.data[0].close).slice(0, 8);
        response.data[0].change = String(response.data[0].change).slice(0, 8);
        this.stockData.push(response.data[0]);
      }
      console.log(this.stockData);
    }
  }
};
</script>
<style></style>
