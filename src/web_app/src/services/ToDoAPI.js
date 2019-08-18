import API from "@/services/API";
export default {
  getToDos() {
    return API().get("todo");
  }
};
