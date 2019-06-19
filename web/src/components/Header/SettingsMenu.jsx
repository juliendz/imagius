import React from "react";

function SettingsMenu() {
    return (
        <li class="nav-item dropdown">
        <a class="nav-link dropdown-toggle" href="#" id="navbarDropdown" role="button" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
          Settings
        </a>
        <div class="dropdown-menu" aria-labelledby="navbarDropdown">
          <a class="dropdown-item" data-toggle="modal" href="#foldermanager-modal">Folder Manager</a>
        </div>
      </li>
    )
}

export default SettingsMenu;
