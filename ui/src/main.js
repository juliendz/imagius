import Vue from 'vue'
import App from './App.vue'
import JQuery from 'jquery'

import store from './store'

import './assets/css/navbar-fixed-right.min.css'

import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap/dist/js/bootstrap.bundle'

window.JQuery = JQuery

Vue.config.productionTip = false

new Vue({
  store,
  render: h => h(App),
}).$mount('#app')
