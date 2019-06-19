import React, {useContext} from "react";
import { observer } from 'mobx-react-lite'

import AppStore from "../../stores/AppStore"
import "./FolderManager.css";

const FolderManager = observer(() => {
  const store = useContext(AppStore)

  const listDirs = store.watchedDirs.map((dir) => 
    <li key={dir.ID} class="list-group-item">{dir.Name}</li>
  )

  return (
    <div
      id="foldermanager-modal"
      class="modal fade foldermanager-modal-lg"
      tabindex="-1"
      role="dialog"
      aria-labelledby="myLargeModalLabel"
      aria-hidden="true"
    >
      <div class="modal-dialog modal-lg" role="document">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title" id="exampleModalLabel">
              Folder Manager
            </h5>
            <button
              type="button"
              class="close"
              data-dismiss="modal"
              aria-label="Close"
            >
              <span aria-hidden="true">&times;</span>
            </button>
          </div>
          <div class="modal-body">
            <div class="card">
              <div class="card-body">
                <div class="container-fluid">
                  <div class="row no-gutters">
                    <div class="col-4">
                      <div class="card">
                        <div class="card-header">Watched folders</div>
                        <div class="card-body">
                            <ul class="list-group">
                                {listDirs}
                            </ul>
                        </div>
                      </div>
                    </div>
                    <div class="col-4" />
                    <div class="col-4" />
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
})

export default FolderManager;