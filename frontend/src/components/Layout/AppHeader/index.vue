<template>
  <v-app-bar 
    app
    dense
    color="primary"
  > 
    <v-app-bar-nav-icon 
      color="white" 
      @click.stop="$emit('showOnlyLogo')"
    />
    <v-toolbar-title class="headline" />
    <v-spacer />
    <ChangeTheme />
  </v-app-bar>
</template>
<script>

import ChangeTheme from '@/components/Layout/AppHeader/ChangeTheme.vue'

export default {
  name: 'AppHeader',
  components: {
    ChangeTheme
  },
}
</script>

<style>
</style>
