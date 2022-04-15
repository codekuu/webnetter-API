<template>
  <v-app>
    <AppSidebar
      :showonlylogo="showonlylogo"
      @showonlylogo="showonlylogo = $event"
    />
    <AppHeader 
      @showonlylogo="showonlylogo = !showonlylogo" 
    />
    <v-content>
      <v-container fluid>
        <transition 
          :key="$route.fullPath" 
          name="fade" 
          mode="out-in"
        >
          <router-view />
        </transition>
      </v-container>
    </v-content>
    <BaseSnackbar />
  </v-app>
</template>

<script>
import AppHeader from '@/components/Layout/AppHeader'
import AppSidebar from '@/components/Layout/AppSidebar'
import BaseSnackbar from '@/components/Common/BaseSnackbar'

export default {
  name: 'App',
  components: {
    AppSidebar,
    BaseSnackbar,
    AppHeader
  },
  data () {
    return {
      showonlylogo: this.$vuetify.breakpoint.smAndUp
    }
  },
  created () {
    this.$vuetify.theme.dark = true
  },
}
</script>
<style>
.fade-enter {
  opacity: 0;
}

.fade-enter-active {
  transition: opacity .1s ease;
}

.fade-leave-active {
  transition: opacity .1s ease;
  opacity: 0;
}

.fwl{
  font-weight: 300!important;
}

.no-wrap{
  white-space: nowrap;
}

.preline{
  white-space: pre-line
}
.underline {
  text-decoration: underline;
}

.pointer {
  cursor: pointer;
}

::-webkit-scrollbar {
  width: 10px;
  height: 10px;
}
::-webkit-scrollbar-button {
  width: 0px;
  height: 0px;
}
::-webkit-scrollbar-thumb {
  background: #e1e1e1;
  border: 0px none #ffffff;
}
::-webkit-scrollbar-thumb:hover {
  background: #f1f1f1;
}
::-webkit-scrollbar-track {
  background: #666666;
  border: 0px none #ffffff;
  border-radius: 0px;
}
::-webkit-scrollbar-corner {
  background: transparent;
}

</style>