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
            <h2 class="portfolio_title">INSERT NAME HERE</h2>
            <p>INSERT USERNAME HERE</p>
          </div>
        </div>
        <div class="portfolio_stocks_container">
          <h2 class="portfolio_title">STOCKS OWNED</h2>
          <hr id="home_hr" />
          <div class="stockowned">
            <div class="stockowned_image_container">
              <img class="stockowned_image" />
            </div>
            <div class="portfolio_stocks_title">
              <h4>COMPANY</h4>
              <h4>PRICE</h4>
              <h4>CHANGE</h4>
              <h4>QUANTITY</h4>
              <h4>AMOUNT</h4>
              <h4>PROFIT</h4>
            </div>
          </div>
          <StockOwned
            v-for="(stock, index) in stocks"
            :key="index"
            v-bind:ticker="stock.ticker"
            v-bind:price="stock.price"
            v-bind:change="stock.change"
            v-bind:quantity="stock.quantity"
            v-bind:amount="stock.amount"
            v-bind:profit="stock.profit"
          ></StockOwned>
        </div>
      </div>
      <div class="portfolio_right_container">
        <div class="portfolio_circlechart_container">
          <h2 class="portfolio_title">PORTFOLIO</h2>
          <hr id="home_hr" />
          <div class="portfolio_donut_chart">
            <DonutChart
              ref="chartchart"
              :chart-data="donutData"
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
export default {
  name: "News", //this is the name of the component
  components: {
    StockOwned: StockOwned,
    LineChart,
    DonutChart
  },
  data() {
    return {
      msg: "Welcome to Finance Boi",
      stocks: [
        {
          ticker: "GOOG",
          price: "1111",
          change: "+5%",
          quantity: "100",
          amount: "10,000",
          profit: "456"
        },
        {
          ticker: "MSFT",
          price: "420",
          change: "+6%",
          quantity: "100",
          amount: "10,000",
          profit: "456"
        },
        {
          ticker: "AMZN",
          price: "5555",
          change: "+10%",
          quantity: "100",
          amount: "10,000",
          profit: "456"
        },
        {
          ticker: "TSLA",
          price: "5555",
          change: "+10%",
          quantity: "100",
          amount: "10,000",
          profit: "456"
        },
        {
          ticker: "GOOGL",
          price: "4455",
          change: "+40%",
          quantity: "100",
          amount: "10,000",
          profit: "456"
        },
        {
          ticker: "AMD",
          price: "1337",
          change: "+69%",
          quantity: "100",
          amount: "10,000",
          profit: "456"
        },
        {
          ticker: "FB",
          price: "1234",
          change: "+44%",
          quantity: "100",
          amount: "10,000",
          profit: "456"
        },
        {
          ticker: "TSLA",
          price: "5555",
          change: "+10%",
          quantity: "100",
          amount: "10,000",
          profit: "456"
        },
        {
          ticker: "GOOGL",
          price: "4455",
          change: "+40%",
          quantity: "100",
          amount: "10,000",
          profit: "456"
        },
        {
          ticker: "AMD",
          price: "1337",
          change: "+69%",
          quantity: "100",
          amount: "10,000",
          profit: "456"
        },
        {
          ticker: "TSLA",
          price: "5555",
          change: "+10%",
          quantity: "100",
          amount: "10,000",
          profit: "456"
        },
        {
          ticker: "GOOGL",
          price: "4455",
          change: "+40%",
          quantity: "100",
          amount: "10,000",
          profit: "456"
        },
        {
          ticker: "AMD",
          price: "1337",
          change: "+69%",
          quantity: "100",
          amount: "10,000",
          profit: "456"
        },
        {
          ticker: "TSLA",
          price: "5555",
          change: "+10%",
          quantity: "100",
          amount: "10,000",
          profit: "456"
        },
        {
          ticker: "GOOGL",
          price: "4455",
          change: "+40%",
          quantity: "100",
          amount: "10,000",
          profit: "456"
        },
        {
          ticker: "AMD",
          price: "1337",
          change: "+69%",
          quantity: "100",
          amount: "10,000",
          profit: "456"
        }
      ],
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
              "rgb(200,0,0,0.3)",
              "rgb(0,200,0,0.3)",
              "rgb(0,0,200,0.3)",
              "rgb(200,200,0,0.3)"
            ],
            data: [1, 2, 3, 4]
          }
        ]
      }
    };
  },
  mounted() {
    this.fillData();
  },
  methods: {
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
              this.getRandomInt(),
              this.getRandomInt(),
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
              this.getRandomInt(),
              this.getRandomInt(),
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
