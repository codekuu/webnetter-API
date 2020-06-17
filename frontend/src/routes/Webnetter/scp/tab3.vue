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
            md="3"
          >
            <v-text-field
              v-model="port"
              label="SSH port"
              outlined
            />
          </v-col>
          <v-col
            cols="12"
            md="3"
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
            md="4"
          >
            <v-text-field
              v-model="username"
              label="SSH Username"
              outlined
            />
          </v-col>
          <v-col
            cols="12"
            md="4"
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
          <v-col
            cols="12"
            md="3"
          >
            <v-text-field
              v-model="location"
              label="SCP location"
              hint="Example, Junos = /var/tmp, Arista = /mnt/flash, Cisco = flash:, nxOS = bootflash:"
              outlined
            />
          </v-col>
          <v-col
            cols="12"
            md="1"
          >
            <v-tooltip top>
              <template v-slot:activator="{ on }">
                <v-btn 
                v-on="on"
                x-large
                :disabled="loading"
                @click="pushHost(IPorHostname, port, software, username, password, location)"
                >
                  <v-icon>mdi-plus</v-icon>
                </v-btn>
              </template>
              <span>Add host to RUN list</span>
            </v-tooltip>
          </v-col>
        </v-row>
      </v-card-text>
      <v-card-actions class="justify-center">
        <v-row>
          <v-col
            cols="12"
            md="4"
          >
          <v-spacer/>
          </v-col>
          <v-col
            cols="8"
            md="2"
          >
            <v-file-input
              @change="handleFileUpload"
              placeholder="Configuration File"
              outlined
              type="file"
              solo
            >
              <template v-slot:selection="{ text }">
                <v-chip
                  label
                  color="primary"
                >
                  {{ text }}
                </v-chip>
              </template>
            </v-file-input>
          </v-col>
          <v-col
            cols="2"
            md="2"
          >
            <v-tooltip top>
              <template v-slot:activator="{ on }">
                <v-btn 
                v-on="on"
                  style="display:block;"
                  :disabled="loading || !hostToConfigure != 0"
                  x-large 
                  @click="runConfiguration()"
                >
                  {{ loading ? 'Running...' : 'Run' }}
                </v-btn>
              </template>
              <span>Run configuration file on Host(s)</span>
            </v-tooltip>
          </v-col>
        </v-row>
      </v-card-actions>
      <v-divider/>
      <BaseTable
      :headers="headers"
      emptyText="Add host(s) by filling out the form above and press on add(+)"
      :items="hostToConfigure"
      />
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
</div>
</template>


<script>
import axios from 'axios'
import snackMessage from '@/api/Error.js'

export default {
  name: 'runCommands',
  data () {
    return {
      file: "",
      hostToConfigure: [],
      showConsole: false,
      showPassword: false,
      loading: false,
      dataFromHost: "",
      headers:[
        { text: 'Host', align: 'center', value: 'host' },
        { text: 'Port', align: 'center', value: 'port' },
        { text: 'Device Type', align: 'center', value: 'device_type' },
        { text: 'SSH Username', align: 'center', value: 'username' },
        { text: 'File location', align: 'center', value: 'location' },
        { text: 'Actions',align: 'right', value: 'action', sortable: false },
      ],
      IPorHostname: "",
      software: "",
      username: "",
      password: "",
      port: 22,
      location: "",
      diffrentSoftware: [
        {text: "Arista eOS", value: "arista_eos"},
        {text: "Cisco IOS", value: "cisco_ios"},
        {text: "Cisco XE", value: "cisco_xe"},
        {text: "Cisco ASA", value: "cisco_asa"},
        {text: "Cisco nxOS", value: "cisco_nxos"},
        {text: "JunOS", value: "juniper_junos"},
        {text: "Linux", value: "linux"},
      ]
    }
  },
  methods: {
    handleFileUpload(event){
      this.file = event
    },
    pushHost(IPorHostname, port, software, username, password, location){
      if (IPorHostname !== '' && port !== '' && software !== '' && username !== '' && password !== '' && location !== '') {
        if (!this.hostToConfigure.some(hosts => hosts.host === IPorHostname)){
          let data = {
            "host" : IPorHostname,
            "username": username,
            "password": btoa(password),
            "device_type": software, 
            "port": port,
            "location": location
          }
          this.hostToConfigure.push(data)
        } else {
          snackMessage("Error", "Host or IP address does already exist.", "red")
        }
      }else{
        snackMessage("Error", "Missing data, try again.", "red")
      }
    },
    runConfiguration() {
      if (this.hostToConfigure.length != 0) {
        this.loading = true
        this.showConsole = false

        const data = new FormData();
        data.append('file', this.file);

        var hostData = JSON.stringify(this.hostToConfigure);
        data.append('hostData', hostData)

        axios.post('/webnetter/scp', data, {headers: {'Content-Type': 'multipart/form-data'}})
          .then((response) => {
            if (response.data.status == "success"){
              snackMessage("Success", "Configuration sent", "green")
              this.loading = false
              this.dataFromHost = response.data.data.dataFromHost
              this.showConsole = true

            }else{
              this.loading = false
              snackMessage("Network Error", response.data.message, "red")
            }
          })
          .catch((error) => {
            this.loading = false
            snackMessage("Network Error", error, "red")
          })
      } else {
        snackMessage("Error", "Missing host(s) in data, try again.", "red")
      }
    },
  },
}
</script>

<style>
</style>
