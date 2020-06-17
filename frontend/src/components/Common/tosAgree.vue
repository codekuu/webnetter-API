<template>
  <v-row justify="end">
    <v-btn
      @click.stop="dialog = true"
    >
      Terms Of Service
    </v-btn>

    <v-dialog
      persistent
      v-model="dialog"
      max-width="95%"
    >
      <v-card>
        <v-card-title class="headline">Terms of Service</v-card-title>

        <v-card-text>
          <br><b>1</b>. The use of the Webnetter is free. Costs may only arise from separate purchases

          <br><b>2</b>. The Webnetter service is provided "as is". None of its users has any kind of claim on the extension and/or modification of the service. In particular, we can not guarantee that the Webnetter service(s) can be accessed from a particular browser and/or operating system.

          <br><b>3</b>. The user of the Webnetter has no claim on the availability and quality of the provided services. As we can not guarantee the correct transmission of data and/or any particular level of performance, no compensation can be provided for the loss of data and potential damage that might occur.

          <br><b>4</b>. The use of the Webnetter is intended for periodic instead of continuous use. Even though there are currently no quotas activated, they might be introduced as the service becomes more popular.

          <br><b>5</b>. All data that is sent by Webnetter goes through our servers where it is available in unencrypted form. We only log information on the sessions opened through Webnetter (such as IP addresses, command and accessed server names) for statistical purposes. The sensible data you send through our system (such as username & passwords) is not being logged. We will not disclose any data to third parties unless they have the legal right of access.

          <br><b>6</b>. It is not allowed to use Webnetter for any kind of malicious act or illegal purpose. In particular it is strictly forbidden to use the provided service for denial-of-service attacks, spamming, break-in attempts and other attacks.
          <br>
          <br><b>7</b>. The service must not be accessed by any kind of automated script or program.
          <br>
          <br><b>8</b>. Any attempt of violating the rules defined in these terms and conditions will be logged and prosecuted.
          <br>
          <br>
          <br>If you have any questions regarding the terms of use outlined here, please do not hesitate to contact root@oppetinternet.se.
        </v-card-text>

          <v-divider/>
          <div align="center">
            <v-btn
              color="red"
              outlined
              class="ma-2"
              @click="disagreeTOS()"
            >
              Disagree
            </v-btn>
            <v-btn
              color="green"
              outlined
              class="ma-2"
              @click="acceptTOS()"
            >
              Agree
            </v-btn>
          </div>
      </v-card>
    </v-dialog>
  </v-row>
</template>

<script>

export default {
  name: 'tosAGREE',
  data () {
    return {
      tab: null,
      dialog: true,
    }
  },
  methods: {
    acceptTOS(){
      this.dialog = false
      localStorage.setItem('acceptTOS', true)
    },
    disagreeTOS(){
      this.dialog = true
      localStorage.setItem('acceptTOS', false)
      this.$router.push({ path: 'home' })
    }
  },
  created(){
    if (localStorage.getItem('acceptTOS') == 'true'){
      this.dialog = false
    }else{
      this.dialog = true
    }
  }
}
</script>