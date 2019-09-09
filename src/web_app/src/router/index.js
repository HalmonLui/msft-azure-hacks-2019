import Vue from "vue";
import Router from "vue-router";
import Home from "@/components/Home";
import ToDo from "@/components/ToDo";
import Portfolio from "@/components/Portfolio";
import Stocks from "@/components/Stocks";
import Login from "@/components/Login";
import Register from "@/components/Register";
import TOS from "@/components/TOS";
import PrivacyPolicy from "@/components/PrivacyPolicy";
import CookiePolicy from "@/components/CookiePolicy";

Vue.use(Router);

export default new Router({
  routes: [
    {
      path: "/",
      name: "Home",
      component: Home
    },
    {
      path: "/portfolio",
      name: "Portfolio",
      component: Portfolio
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
    },
    {
      path: "/tos",
      component: TOS
    },
    {
      path: "/privacypolicy",
      component: PrivacyPolicy
    },
    {
      path: "/cookiepolicy",
      component: CookiePolicy
    }
  ]
});
