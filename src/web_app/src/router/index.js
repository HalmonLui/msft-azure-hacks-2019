import Vue from "vue";
import Router from "vue-router";
import Home from "@/components/Home";
import ToDo from "@/components/ToDo";
import Portfolio from "@/components/Portfolio";
import Stocks from "@/components/Stocks";
import Profile from "@/components/Profile";
import Login from "@/components/Login";
import Register from "@/components/Register";
import TOS from "@/components/TOS";
import PrivacyPolicy from "@/components/PrivacyPolicy";
import CookiePolicy from "@/components/CookiePolicy";
import firebase from "firebase";

Vue.use(Router);

const router = new Router({
  routes: [
    {
      //Redirects path to /login if user enters invalid path
      path: "*",
      redirect: "/"
    },
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
      path: "/profile",
      name: "Profile",
      component: Profile
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

// Makes some pages required for loggin in first
/*router.beforeEach((to, from, next) => {
  const currentUser = firebase.auth().currentUser;
  const requiresAuth = to.matched.some(record => record.meta.requiresAuth);

  if (requiresAuth && !currentUser) next('login');
  else if (!requiresAuth && currentUser) next('home');
  else next();
});*/

export default router;
