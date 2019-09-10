import API from "@/services/API";
export default {
  getStocks() {
    return API().get("stocks");
  }
};
