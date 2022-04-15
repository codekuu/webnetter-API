<template>
  <v-btn
    icon
    @click="$vuetify.theme.dark = !$vuetify.theme.dark"
  >
    <v-icon>fa-adjust<v-icon /></v-icon>
  </v-btn>
</template>

<script>
export default {
  name: 'XXXXX',
  props: {
    yaBoi: {
      type: [String, Number],
      default: ''
    },
  },
  data () {
    return {
      x1: 'deleteme?'
    }
  },
  computed: {
    x3 () {
      return 0
    }
  },
  methods: {
    x2 () {

    }
  }
}
</script>

<style>
</style>

