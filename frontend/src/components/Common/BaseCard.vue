<template>
  <v-container>
    <v-layout
      text-center
      wrap
    >
      <v-col 
        cols="12" 
        lg="10"
        offset-lg="1"
        offset-xl="0"
        xl="12"
      >
        <v-card>
          <slot name="header" />
          <v-card-title
            v-if="title"
            class="title font-weight-light"
          >
            <div>
              {{ title }}
            </div>
            <slot name="title" />
          </v-card-title>
          <slot />
          <slot name="footer" />
        </v-card>
      </v-col>
    </v-layout>
  </v-container>
</template>
<script>
export default {
  name: 'BaseCard',
  props: {
    title: {
      type: [String],
      default: ''
    }
  }
}
</script>