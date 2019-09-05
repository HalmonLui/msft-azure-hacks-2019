import API from "@/services/API";
export default {
  getNews() {
    return API().get("news");
  }
};
