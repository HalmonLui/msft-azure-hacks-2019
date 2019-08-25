<template>
  <div>
    <hr id="home_hr" />
    <div>
      <p>Search: Bing Search Boi In Here</p>
    </div>
    <hr id="home_hr" />
    <Stocklist
      v-for="stock in stocks"
      v-bind:symbol="stock.symbol"
      v-bind:price="stock.price"
      v-bind:change="stock.change"
    ></Stocklist>
  </div>
</template>

<script>
import Stocklist from "./subcomponents/Stocklist";
import Stock from "./subcomponents/Stock";
export default {
  name: "Stocks", //this is the name of the component
  components: {
    Stocklist: Stocklist,
    Stock: Stock
  },
  data() {
    return {
      stocks: [
        { symbol: "MSFT", price: "420", change: "+6%" },
        { symbol: "MSFT", price: "420", change: "+6%" },
        { symbol: "AMZN", price: "5555", change: "+10%" },
        { symbol: "TSLA" },
        { symbol: "KEVT" },
        {},
        {},
        {},
        {},
        {},
        {},
        {},
        {},
        {},
        {},
        {},
        {},
        {},
        {},
        {},
        {},
        {},
        {},
        {},
        {},
        {},
        {},
        {},
        {},
        {}
      ]
    };
  }
};
</script>
<style></style>
