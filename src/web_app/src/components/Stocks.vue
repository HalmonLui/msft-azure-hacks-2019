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
          v-bind:symbol="stock.symbol"
          v-bind:price="stock.price"
          v-bind:change="stock.change"
        ></Stocklist>
      </div>
      <div class="stocks_watchlist_container">
        <h2 class="home_watchlist_title">Watch List</h2>
        <WatchItem
          v-for="(watchitem, index) in watchitems"
          :key="index"
          v-bind:symbol="watchitem.symbol"
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
export default {
  name: "Stocks", //this is the name of the component
  components: {
    Stocklist: Stocklist,
    WatchItem: WatchItem
  },
  data() {
    return {
      stocks: [
        { symbol: "GOOG", price: "1111", change: "+5%" },
        { symbol: "MSFT", price: "420", change: "+6%" },
        { symbol: "AMZN", price: "5555", change: "+10%" },
        { symbol: "TSLA", price: "5555", change: "+10%" },
        { symbol: "KEVT", price: "4455", change: "+40%" },
        { symbol: "SNAM", price: "1337", change: "+69%" },
        { symbol: "BRHE", price: "1234", change: "+44%" },
        { symbol: "GOOG", price: "1111", change: "+5%" },
        { symbol: "MSFT", price: "420", change: "+6%" },
        { symbol: "AMZN", price: "5555", change: "+10%" },
        { symbol: "TSLA", price: "5555", change: "+10%" },
        { symbol: "KEVT", price: "4455", change: "+40%" },
        { symbol: "SNAM", price: "1337", change: "+69%" },
        { symbol: "BRHE", price: "1234", change: "+44%" },
        { symbol: "GOOG", price: "1111", change: "+5%" },
        { symbol: "MSFT", price: "420", change: "+6%" },
        { symbol: "AMZN", price: "5555", change: "+10%" },
        { symbol: "TSLA", price: "5555", change: "+10%" },
        { symbol: "KEVT", price: "4455", change: "+40%" },
        { symbol: "SNAM", price: "1337", change: "+69%" },
        { symbol: "BRHE", price: "1234", change: "+44%" },
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
      ]
    };
  }
};
</script>
<style></style>
