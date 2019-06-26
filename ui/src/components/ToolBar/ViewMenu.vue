<template>
    <li class="nav-item dropdown">
        <a class="nav-link dropdown-toggle" href="#" id="navbarDropdown" role="button" data-toggle="dropdown"
            aria-haspopup="true" aria-expanded="false">
            View
        </a>
        <div class="dropdown-menu" aria-labelledby="navbarDropdown">
            <a class="dropdown-item" v-on:click="showPropertiesSideBar" href="#">Properties</a>
        </div>
    </li>
</template>

<script>

export default {
    name: "ViewMenu",
    data: function() {
        return {}
    },
    methods: {
        showPropertiesSidebar() {
            
        }
    }
}
</script>
