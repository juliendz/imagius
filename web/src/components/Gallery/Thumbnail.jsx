import React from "react";
import "./Thumbnail.css";

function Thumbnail(props) {
  return (
    <div class="img-thumb">
        <img src={props.source} class="img-thumbnail" alt="..."></img>
    </div>
  );
}

export default Thumbnail;
