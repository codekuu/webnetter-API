<template>
  <div>
    <v-tabs
      v-model="tab"
      color="#1c85b7"
    >
      <v-tab
        v-for="item in items"
        :key="item"
      >
        {{ item }}
      </v-tab>
    </v-tabs>
    <v-tabs-items v-model="tab">

      <!-- TAB ONE -->
      <v-tab-item>
        <runCommandsTab1/>
      </v-tab-item>

      <!-- TAB TWO -->
      <v-tab-item>
        <v-card>
          <configureTab2/>
        </v-card>
      </v-tab-item>

      <v-tab-item>
        <v-card>
          <scpTab3/>
        </v-card>
      </v-tab-item>

    </v-tabs-items>
</div>
</template>


<script>

export default {
  name: 'Webnetter',
  data () {
    return {
      tab: null,
      items: [
        'Run Command', 'Configure', 'Scp'
      ],
    }
  }
}
</script>

<style>
</style>
