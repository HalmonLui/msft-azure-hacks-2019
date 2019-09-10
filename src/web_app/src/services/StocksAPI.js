import API from "@/services/API";
export default {
  getStocks() {
    return API().get("stocks");
  },
  getStock(ticker) {
    return API().get("stock", { params: { ticker: ticker } });
  }
};
