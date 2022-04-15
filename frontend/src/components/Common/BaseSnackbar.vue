<template>
  <v-snackbar
    :value="$store.getters.snackShow"
    :vertical="!!$store.getters.snackMessage"
    :timeout="$store.getters.snackTimeout"
    :color="$store.getters.snackColor"
    bottom
    class="pb-5 mb-5"
  >
    <div class="title ma-0">
      {{ $store.getters.snackTitle }}
    </div>
    <!-- eslint-disable-next-line --> <!-- we disable linter because of the preline class -->
    <div class="subtitle-1 preline">{{ $store.getters.snackMessage ? $store.getters.snackMessage : '' }}</div>
    <v-btn
      v-if="$store.getters.snackUndoLength"
      text
      @click="$store.dispatch('snackUndoCallback')"
    >
      Undo
    </v-btn>
    <v-btn
      v-else
      text
      class="ma-0"
      @click="$store.commit('snackShow', false)"
    >
      <v-icon>close</v-icon>
    </v-btn>
  </v-snackbar>
</template>
<script>
export default {
  computed: {
    snackShow: {
      // getter
      get () {
        return this.$store.getters.snackShow
      },
      // setter
      set (nV) {
        return this.$store.commit('snackShow', nV)
      }
    }
  }
}
</script>
