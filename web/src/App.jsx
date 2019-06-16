import React from 'react';
import logo from './logo.svg';
import './App.css';
import './bulma.css';

import FolderManager from './components/FolderManager/FolderManager'

function App() {
    return ( 
        <div class = "App">
            <div class = "columns is-gapless">
                <div id="left-column" class = "column is-2"> 
                    <div id="left-content" class="panel">
                        <p class="panel-heading">
                            Folders
                        </p>
                        <div class="panel-block">

                        </div>
                    </div>
                 </div> 
                <div class = "column"> 
                    <div id="right-content" class="box">
                    </div>
                </div> 
            </div>
        </div>
    );
}

export default App;