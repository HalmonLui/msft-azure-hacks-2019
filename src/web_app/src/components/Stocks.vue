<template>
  <div class="stocks">
    <hr id="home_hr" />
    <div>
      <p>Search: Bing Search Boi In Here</p>
    </div>
    <hr id="home_hr" />
    <div class="stocks_body">
      <div class="stocks_stockslist_container">
        <Stocklist
          v-for="stock in stocks"
          v-bind:symbol="stock.symbol"
          v-bind:price="stock.price"
          v-bind:change="stock.change"
        ></Stocklist>
      </div>
      <div class="stocks_watchlist_container">
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
