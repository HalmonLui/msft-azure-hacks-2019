import API from "@/services/API";
export default {
  addStock(user, stock) {
    return API().post("addStock", { user: user, stock: stock });
  }
};
