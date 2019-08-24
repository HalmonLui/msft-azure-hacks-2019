import Vue from "vue";
import Router from "vue-router";
import Home from "@/components/Home";
import ToDo from "@/components/ToDo";
import News from "@/components/News";
import Stocks from "@/components/Stocks";
import Login from "@/components/Login";
import Register from "@/components/Register";

Vue.use(Router);

export default new Router({
  routes: [
    {
      path: "/",
      name: "Home",
      component: Home
    },
    {
      path: "/news",
      name: "News",
      component: News
    },
    {
      path: "/stocks",
      name: "Stocks",
      component: Stocks
    },
    {
      path: "/login",
      name: "Login",
      component: Login
    },
    {
      path: "/register",
      name: "Register",
      component: Register
    },
    {
      path: "/todo",
      component: ToDo
    }
  ]
});
