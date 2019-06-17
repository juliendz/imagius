import React from "react";
import {Link} from "react-router-dom"

function SettingsMenu() {
    return (
        <li class="nav-item dropdown">
        <a class="nav-link dropdown-toggle" href="#" id="navbarDropdown" role="button" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
          Settings
        </a>
        <div class="dropdown-menu" aria-labelledby="navbarDropdown">
          <a class="dropdown-item" href="#">Folder Manager</a>
        </div>
      </li>
    )
}

export default SettingsMenu;
