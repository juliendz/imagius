import Vue from 'vue'
import Vuex from 'vuex'

import websocketPlugin from "./websocketPlugin"

Vue.use(Vuex);

const wsPlugin = websocketPlugin(new WebSocket("ws://localhost:1323/ws"))

export default new Vuex.Store({
    state: {

        errors: {
        },
        "WATCHEDFOLDERS": [],
    },
    mutations: {
        GET_WATCHED(state) {
        }, 
        SET_WATCHED(state, watchedDirs) {
            WATCHEDFOLDERS = watchedDirs
        },
    },
    actions: {
    },
    plugins: [wsPlugin]
})
