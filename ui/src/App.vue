<template>
  <div id="app">
      <Gallery />
      <FolderManager />
  </div>
</template>

<script>
import Gallery from './components/Gallery/Gallery'
import FolderManager from './components/FolderManager/FolderManager'

export default {
  name: 'app',
  components: {
      Gallery,
      FolderManager
  }
}
</script>

<style>
</style>
