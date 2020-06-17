<template>
  <div>
    <v-card>
      <v-card-text>
        <v-row>
          <v-col
            cols="8"
            md="6"
          >
            <v-text-field
              v-model="IPorHostname"
              label="IP address/ Hostname"
              hint="Can be either hostname or ip address."
              outlined
            />
          </v-col>
          <v-col
            cols="4"
            md="2"
          >
            <v-text-field
              v-model="port"
              label="SSH port"
              outlined
            />
          </v-col>
          <v-col
            cols="12"
            md="4"
          >
            <v-select
              v-model="software"
              :items="diffrentSoftware"
              label="Software on host"
              outlined
            />
          </v-col>
        </v-row>
        <v-row>
          <v-col
            cols="12"
            md="6"
          >
            <v-text-field
              v-model="username"
              label="SSH Username"
              outlined
            />
          </v-col>
          <v-col
            cols="12"
            md="6"
          >
            <v-text-field
              v-model="password"
              :append-icon="showPassword ? 'visibility' : 'visibility_off'"
              :type="showPassword ? 'text' : 'password'"
              outlined
              hint="Password is encrypted with base64 on call over SSL."
              name="input-10-1"
              label="SSH Password"
              @click:append="showPassword = !showPassword"
            />
          </v-col>
        </v-row>
        <v-row>
          <v-col
            cols="12"
            md="12"
          >
            <v-text-field
              v-model="command"
              label="Command to run"
              outlined
            />
          </v-col>
        </v-row>
      </v-card-text>
      <v-card-actions class="justify-center">
        <v-btn 
        style="display:block;"
          :disabled="loading"
          x-large 
          @click="runCommand(IPorHostname, port, software, username, password, command)"
        >
          {{ loading ? 'Fetching Data...' : 'Run' }}
        </v-btn>
      </v-card-actions>
      <div v-if="loading">
        <v-progress-linear
          indeterminate
          color="blue"
        />
      </div>
      <v-textarea
        style="font: 16px monospace;!important"
        v-if="showConsole"
        :value="dataFromHost"
        name="input-7-1"
        class="ml-4 mr-4"
        filled
        readonly
        label="Console: "
        auto-grow
      />
    </v-card>
    <BaseCard v-if="showLoop">
      <v-data-table
        :headers="headers"
        :items="dataFromHostLoop"
        :items-per-page="5"
        class="elevation-1"
      ></v-data-table>
    </BaseCard>
</div>
</template>


<script>
import axios from 'axios'
import snackMessage from '@/api/Error.js'

export default {
  name: 'runCommands',
  data () {
    return {
      software: "",
      command: "display interface brief",
      showPassword: false,
      IPorHostname: "",
      username: "",
      loading: false,
      dataFromHost: "",
      showLoop: false,
      dataFromHostLoop: [
                        {"aging":"20", "vlan":"33", "mac":"abcd-1234-abcd"}, 
                        {"aging":"45", "vlan":"13", "mac":"abcd-1234-efgh"}, 
                        {"aging":"10", "vlan":"23", "mac":"efgh-abcd-4567"}
                        ],
      showConsole: false,
      password: "",
      port: 22,
      diffrentSoftware: [
        {text: "Arista eOS", value: "arista_eos"},
        {text: "Cisco IOS", value: "cisco_ios"},
        {text: "Cisco XE", value: "cisco_xe"},
        {text: "Cisco ASA", value: "cisco_asa"},
        {text: "Cisco nxOS", value: "cisco_nxos"},
        {text: "Fortinet", value: "fortinet"},
        {text: "HP Comware", value: "hp_comware"},
        {text: "HP Procurve", value: "hp_procurve"},
        {text: "Juniper", value: "juniper"},
        {text: "JunOS", value: "juniper_junos"},
        {text: "Linux", value: "linux"}
      ]
    }
  },
  computed:{
    headers () {
    if (this.dataFromHostLoop.length) {
      return Object.keys(this.dataFromHostLoop[0]).map(row => {
        return {
          text: row.toUpperCase(),
          value: row,
        }
      })
    }
    return []
    
    }
  },
  methods: {
    runCommand(IPorHostname, port, software, username, password, command) {
      if (IPorHostname !== '' && port !== '' && software !== '' && username !== '' && password !== '' && command ) {
        let data = {
          "host" : IPorHostname,
          "username": username,
          "password": btoa(password),
          "device_type": software, 
          "port": port,
          "command": command
        }
        this.loading = true
        this.showConsole = false
		this.showLoop = false
        axios.post('/webnetter/runcommand', data)
          .then((response) => {
            if (response.data.status == "success"){
              snackMessage("Success", "Success, session closed towards " + IPorHostname, "green")
              this.loading = false
             
              if (typeof(response.data.data.dataFromHost) == "string"){
                this.dataFromHost = response.data.data.dataFromHost
                this.showConsole = true
                this.showLoop = false
              }else{
                this.dataFromHostLoop = response.data.data.dataFromHost
                this.showLoop = true
              }
            }else{
              this.loading = false
              snackMessage("Network Error", response.data.message, "red")
              this.showConsole = false
            }
          })
          .catch((error) => {
            this.loading = false
            snackMessage("Network Error", error, "red")
          })
      } else {
        snackMessage("Error", "Missing data in request, try again.", "red")
      }
    },
  },
}
</script>

<style>
</style>
