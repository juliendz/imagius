import React from "react";
import "./Gallery.css";

import GalleryHeader from "./GalleryHeader"
import GalleryView from "./GalleryView"

function Gallery() {
  return (
    <div class="card">
      <div class="card-body">
        <div class="container-fluid">
          <div class="row no-gutters">
            <div class="col-12">
                <GalleryHeader />
                <GalleryView />
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Gallery;

