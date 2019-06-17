import React from "react";
import "./Thumbnail.css";

function Thumbnail(props) {
  return (
    <div class="img-thumb float-left">
        <img src={props.source} class="img-thumbnail" alt="..."></img>
    </div>
  );
}

export default Thumbnail;

