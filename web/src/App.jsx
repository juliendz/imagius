import React, {Component} from "react";
import "./App.css";

import "bootstrap/dist/css/bootstrap.min.css";
import "bootstrap/dist/js/bootstrap.bundle";

import FolderManager from "./components/FolderManager/FolderManager";
import Header from "./components/Header/Header.jsx";
import Gallery from "./components/Gallery/Gallery";

class App extends Component {

   constructor(props){
       super(props)
    }

    componentDidMount() {
        const socket = new WebSocket("ws://localhost:1323/ws")
        socket.onopen = function(event){
            console.log("OPEN")
            socket.send("GETWATCHED")
        }
        socket.onmessage = function(event){
            console.log("MESSAGE: ", event.data)
        }
        socket.onclose = function(event){
            console.log("CLOSE")
        }
        socket.onerror = function(event){
            console.log("ERROR:", event.message)
        }
    }

  render (){
    return <div class="App">
        <div class="container-fluid">
          <div class="row">
            <div class="col">
              <div class="box">
                <Header />
              </div>
            </div>
          </div>
          <div class="row no-gutters">
            <div class="col-2">
              <div id="left-content" class="panel">
                <div class="card">
                  <div class="card-header">Folders</div>
                  <div class="card-body" />
                </div>
              </div>
            </div>
            <div class="col-10">
              <div id="right-content" class="box">
                  <Gallery />
              </div>
            </div>
          </div>
        </div>
        <FolderManager />
    </div>
  }
}

export default App;
