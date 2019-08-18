import Vue from "vue";
import Router from "vue-router";
import HelloWorld from "@/components/HelloWorld";
import ToDo from "@/components/ToDo";
Vue.use(Router);
export default new Router({
  routes: [
    {
      path: "/",
      name: "HelloWorld",
      component: HelloWorld
    },
    {
      path: "/todo",
      component: ToDo
    }
  ]
});
