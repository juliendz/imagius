import Helpers from "./helpers"

export default function webSocketPlugin (socket) {
    return store => {

        socket.onopen = function(event){
            console.log("OPEN")
        }
        socket.onmessage = function(event){

            var operation = JSON.parse(event.data)
            console.log("MESSAGE: ", operation)

            switch(operation.cmd) {
                case "DATA_WATCHED":
                    store.commit("SET_WATCHED", operation.payload)
            }

        }
        socket.onclose = function(event){
            console.log("CLOSE", event.code)
        }
        socket.onerror = function(event){
            console.log("ERROR:", event.message)
        }

        store.subscribe((mutation, state) => {

            console.log(mutation)
            switch(mutation.type) {

                case "GET_WATCHED":
                    console.log("====> GET_WATCHED")
                    var cmd = {
                        "cmd": "GET_WATCHED",
                    "payload":  []
                    }
                    socket.send(JSON.stringify(cmd))
                    break

                case "ADD_WATCHED":
                    var op = Helpers.makeOperation("ADD_WATCHED", mutation.payload)
                    console.log("====> ADD_WATCHED ", op)
                    socket.send(op)
                    break

                case "DEL_WATCHED":
                    var op = Helpers.makeOperation("DEL_WATCHED", mutation.payload)
                    console.log("====> DEL_WATCHED ", op)
                    socket.send(op)
                    break
            }
        })

    }
}