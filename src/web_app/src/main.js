// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
import router from './router'

import firebase from 'firebase';

Vue.config.productionTip = false

let app = '';
// Your web app's Firebase configuration
firebase.initializeApp({
  apiKey: "AIzaSyD9vM-27W3kyeRqKJ7GijGe9ldLncZqOmk",
  authDomain: "vue-firebase-tutorial-9eced.firebaseapp.com",
  databaseURL: "https://vue-firebase-tutorial-9eced.firebaseio.com",
  projectId: "vue-firebase-tutorial-9eced",
  storageBucket: "",
  messagingSenderId: "578857354586",
  appId: "1:578857354586:web:d11f71fc2f26eb84925f63"
});

firebase.auth().onAuthStateChanged(() => {
  if(!app) {
    app = new Vue({
      el: '#app',
      router,
      components: { App },
      template: '<App/>'
    })
  }
});
/* eslint-disable no-new */
