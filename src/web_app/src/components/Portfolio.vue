<template>
  <div>
    <hr id="home_hr" class="portfolio_hr" />
    <div class="portfolio">
      <div class="portfolio_left_container">
        <div class="portfolio_user_container">
          <div class="portolio_image_container">
            <img
              src="https://petcube.com/blog/content/images/2018/05/cute-cat-behavior-laying-on-the-back.jpg"
              class="portfolio_image"
            />
          </div>
          <div class="portfolio_user_text_container">
            <h2 class="portfolio_title">Hello, {{ user }}</h2>
            <p class="portfolio_description">
              Welcome back to Finance Boi! To add to the stock watchlist, visit
              the Stocks tab. To read financial news, visit the Home tab. To see
              how to optimize your portfolio for lowest volatility or maximum
              risk, stay here! User investment capital calculations and profit
              over time coming soon.
            </p>
          </div>
        </div>
        <div class="portfolio_stocks_container">
          <h2 class="portfolio_title">STOCKS OWNED</h2>
          <hr id="home_hr" />
          <div class="stockowned" id="stockowned_title">
            <div class="stockowned_image_container">
              <img class="stockowned_image" />
            </div>
            <div class="portfolio_stocks_title">
              <h4>COMPANY</h4>
              <h4>PRICE</h4>
              <h4>CHANGE</h4>
              <h4>QUANTITY</h4>
              <!--
              <h4>AMOUNT</h4>
              <h4>PROFIT</h4>-->
            </div>
          </div>
          <h2 v-if="loading">Loading stocks...</h2>
          <StockOwned
            v-for="(stock, index) in stocks"
            :key="index"
            v-bind:ticker="stocks[index].ticker"
            v-bind:price="stocks[index].close"
            v-bind:change="stocks[index].change"
            v-bind:quantity="stocks[index].quantity"
            v-bind:amount="stocks[index].amount"
            v-bind:profit="stocks[index].profit"
          ></StockOwned>
        </div>
      </div>
      <div class="portfolio_right_container">
        <div class="portfolio_circlechart_container">
          <h2 class="portfolio_title">LOW VOLATILITY</h2>
          <hr id="home_hr" />
          <div class="portfolio_donut_chart">
            <DonutChart
              ref="chartchart"
              :chart-data="donutData"
              :options="options"
            ></DonutChart>
          </div>
        </div>
        <div class="portfolio_circlechart_container">
          <h2 class="portfolio_title">MAXIMUM RISK</h2>
          <hr id="home_hr" />
          <div class="portfolio_donut_chart">
            <DonutChart
              ref="chartchart"
              :chart-data="maximumRiskData"
              :options="options"
            ></DonutChart>
          </div>
        </div>
        <div class="portfolio_graphs_container">
          <div class="portfolio_graph_container">
            <div class="portfolio_line_graph">
              <line-chart :chart-data="msft_data"></line-chart>
            </div>
          </div>
          <div class="portfolio_graph_container">
            <div class="portfolio_line_graph">
              <line-chart :chart-data="portfolio_worth_data"></line-chart>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import LineChart from "./charts/LineChart.js";
import DonutChart from "./charts/DonutChart";
import StockOwned from "./subcomponents/StockOwned";
import StocksAPI from "@/services/StocksAPI.js";
import UserAPI from "@/services/UserAPI.js";
import firebase from "firebase";

export default {
  name: "Portfolio", //this is the name of the component
  components: {
    StockOwned: StockOwned,
    LineChart,
    DonutChart
  },
  data() {
    return {
      msg: "Welcome to Finance Boi",
      user: null,
      loading: true,
      watchitems: [],
      stocks: [],
      msft_data: null,
      portfolio_worth_data: null,
      options: {
        responsive: true,
        maintainAspectRatio: false,
        animation: {
          animateRotate: false
        }
      },
      donutData: {
        labels: ["AMZN", "GOOG", "MSFT", "TSLA"],
        datasets: [
          {
            backgroundColor: [
              "#81C784",
              "#4DB6AC",
              "#4DD0E1",
              "#4FC3F7",
              "#64B5F6",
              "#7986CB",
              "#9575CD",
              "#BA68C8",
              "#F06292",
              "#e57373",
              "#AED581",
              "#DCE775",
              "#FFF176",
              "#FFD54F",
              "#FFB74D"
            ],
            data: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
          }
        ]
      },
      maximumRiskData: {
        labels: ["AMZN", "GOOG", "MSFT", "TSLA"],
        datasets: [
          {
            backgroundColor: [
              "#81C784",
              "#4DB6AC",
              "#4DD0E1",
              "#4FC3F7",
              "#64B5F6",
              "#7986CB",
              "#9575CD",
              "#BA68C8",
              "#F06292",
              "#e57373",
              "#AED581",
              "#DCE775",
              "#FFF176",
              "#FFD54F",
              "#FFB74D"
            ],
            data: [1, 2, 3, 4, 3, 2, 1, 2, 3, 4, 3, 2, 1, 2, 3]
          }
        ]
      },
      lowVolatilityData: {
        labels: [],
        datasets: [
          {
            backgroundColor: [],
            data: []
          }
        ]
      }
    };
  },
  mounted() {
    this.fillData();
    this.getUser();
    this.getWatchlist();
  },
  methods: {
    getUser() {
      var user = firebase.auth().currentUser;
      this.user = user.email;
    },
    async getWatchlist() {
      const watchitems = await UserAPI.getWatchlist(this.user);
      for (var i = 0; i < watchitems.data[0].stocks.length; i++) {
        this.watchitems.push(watchitems.data[0].stocks[i]);
      }
      this.loadStocks();
      this.loading = false;
      console.log(this.stocks);
    },
    async loadStocks() {
      for (var item in this.watchitems) {
        const response = await StocksAPI.getStock(this.watchitems[item].ticker);
        response.data[0].close = String(response.data[0].close).slice(0, 8);
        response.data[0].change = String(response.data[0].change).slice(0, 8);
        this.stocks.push(response.data[0]);
      }
    },
    fillData() {
      this.msft_data = {
        labels: [this.getRandomInt(), this.getRandomInt()],
        datasets: [
          {
            label: "MSFT",
            backgroundColor: "rgb(100,0,200,0.3)",
            data: [
              this.getRandomInt(),
              this.getRandomInt(),
              this.getRandomInt()
            ]
          }
        ]
      };
      this.portfolio_worth_data = {
        labels: [this.getRandomInt(), this.getRandomInt()],
        datasets: [
          {
            label: "Portfolio Worth",
            backgroundColor: "rgb(0,256,0,0.3)",
            data: [
              this.getRandomInt(),
              this.getRandomInt(),
              this.getRandomInt()
            ]
          }
        ]
      };
    },
    getRandomInt() {
      return Math.floor(Math.random() * 100);
    }
  }
};
</script>
<style></style>
