<template>
    <div id="foldermanager-modal" class="modal fade foldermanager-modal-lg" tabindex="-1" role="dialog"
        aria-labelledby="myLargeModalLabel" aria-hidden="true">
        <div class="modal-dialog modal-lg" role="document">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title" id="exampleModalLabel">
                        Folder Manager
                    </h5>
                    <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                        <span aria-hidden="true">&times;</span>
                    </button>
                </div>
                <div class="modal-body">
                    <div class="container-fluid">
                        <div class="row no-gutters">
                            <div class="col-6">
                                <div class="card">
                                    <div class="card-header">Watched folders</div>
                                    <div class="card-body">
                                        <ul class="list-group">
                                            <li v-for="f in watchedFolders" v-bind:key="f.ID" class="list-group-item">
                                                {{f.Name}}</li>
                                        </ul>
                                        <div>
                                            <button v-on:click="addFolder" type="button" class="btn btn-primary btn-sm">Add Folder</button>
                                            <button type="button" class="btn btn-secondary btn-sm">Remove Folder</button>
                                            <input v-on:change="onSelectedFolder" type="file" style="display:none" id="addFolderInput" webkitdirectory/>
                                        </div>
                                    </div>
                                </div>
                            </div>
                            <div class="col-6" />
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
    export default {
        name: "FolderManager",
        data: function () {
            return {
            }
        },
        computed: {
            watchedFolders() {
                return this.$store.state.WatchedFolders
            }
        },
        methods: {
            addFolder() {
                console.log("sdf")
                document.getElementById("addFolderInput").click()
            },
            onSelectedFolder(e) {
                console.log(e.target.files[0].path)
            }
        }
    }
</script>