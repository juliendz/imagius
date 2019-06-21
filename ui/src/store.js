import Vue from 'vue'
import Vuex from 'vuex'

import websocketPlugin from "./websocketPlugin"

Vue.use(Vuex);

const wsPlugin = websocketPlugin(new WebSocket("ws://localhost:1323/ws"))

export default new Vuex.Store({
    state: {

        errors: {
        },
        "WatchedFolders": [],
    },
    mutations: {
        GET_WATCHED(state) {
        }, 
        SET_WATCHED(state, watchedDirs) {
            state.WatchedFolders = watchedDirs
        },
        ADD_WATCHED(state, newDir){ },
        DEL_WATCHED(state, dirId){ },
    },
    actions: {
    },
    plugins: [wsPlugin]
})
