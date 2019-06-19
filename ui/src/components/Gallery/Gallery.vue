<template>
        <div class="container-fluid">
          <div class="row">
            <div class="col">
              <div class="box">
                  <ToolBar />
              </div>
            </div>
          </div>
          <div class="row no-gutters">
            <div class="col-2">
              <div id="left-content" class="panel">
                <div class="card">
                  <div class="card-header">Folders</div>
                  <div class="card-body">
                  </div>
                </div>
              </div>
            </div>
            <div class="col-10">
              <div id="right-content" class="box">
              </div>
            </div>
          </div>
        </div>
</template>

<script>
import ToolBar from "../ToolBar/ToolBar"

export default {
    name: "Gallery",
    components: {
        ToolBar
    }
};
</script>

<style>

#left-content {
    border: 1px solid gray;
    height: 94vh;
}

#right-content {
    border-top: 1px solid gray;
    border-bottom: 1px solid gray;
    border-right: 1px solid gray;
    height: 94vh;
}
</style>