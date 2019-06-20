<template>
    <li class="nav-item dropdown">
        <a class="nav-link dropdown-toggle" href="#" id="navbarDropdown" role="button" data-toggle="dropdown"
            aria-haspopup="true" aria-expanded="false">
            Settings
        </a>
        <div class="dropdown-menu" aria-labelledby="navbarDropdown">
            <a class="dropdown-item" v-on:click="showFolderManagerModal" href="#">Folder Manager</a>
        </div>
    </li>
</template>

<script>

export default {
    name: "SettingsMenu",
    data: function() {
        return {}
    },
    methods: {
        showFolderManagerModal: function() {
            this.$store.commit("GET_WATCHED")
            JQuery('#foldermanager-modal').modal()
        }
    }
}
</script>
