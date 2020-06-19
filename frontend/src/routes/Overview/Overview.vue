<template>
  <BaseCard>
    <v-row>
      <v-card
        class="mx-auto"
        flat
      >
        <v-card-title class="justify-center display-1 font-weight-thin">
          <b>Webnetter API</b>
        </v-card-title>
        <v-card-text>
          <br>Webnetter API is a network management API built on Netmiko.
          <br>Built for communication and configuration of devices.
          <br>
          <br>Backend made with only love for Python <v-icon>mdi-heart</v-icon>
          <br>
        </v-card-text>
        <v-card-actions class="justify-center">
          <v-btn
            x-large
            @click="$router.push({name:'webnetter'})"
          >
            <v-icon>
              mdi-server
            </v-icon>
            Try it out
          </v-btn>
          <v-btn
            x-large 
            href="https://github.com/codekuu/webnetter-api"
          >
            <v-icon>
              fa-book
            </v-icon>
            Documentation
          </v-btn>
        </v-card-actions>
        <br>
      </v-card>
    </v-row>
  </BaseCard> 
</template>
<script>
export default {
  name: 'Overview',

}
</script>

<style>
</style>
