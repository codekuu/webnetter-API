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
            md="5"
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
                @click="pushHost(IPorHostname, port, software, username, password)"
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
              accept=".txt,.conf,.cfg"
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
      <v-row justify="end">
        <v-col
          cols="2"
          md="2"
        >
          <v-file-input
            @change="importExcel()"
            placeholder="Import Excel"
            outlined
            dense
            flat
            type="file"
            accept=".xls,.xlsx"
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
          cols="1"
          md="1"
        >
          <v-btn dense :disabled="!excelFile" @click="pushExcel()">ADD</v-btn>
        </v-col>
      </v-row>
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
      <div class="pa-3" v-if="showSummary">
        <h2>Summary: </h2>
        <br/>
        <v-expansion-panels v-if="showSummary" focusable multiple>
          <v-expansion-panel
            v-for="(host,i) in hosts"
            :key="i"
          >
            <v-expansion-panel-header hide-actions disable-icon-rotate>
              <div>
                <v-icon v-if="host.success" color="success">mdi-server</v-icon>
                <v-icon v-else color="error">mdi-server</v-icon>
                <span>{{ host.host }}</span>
              </div>
            </v-expansion-panel-header>
            <v-expansion-panel-content>
              <v-row>
                <v-col
                  cols="3"
                  md="3"
                >
                  <v-text-field
                    v-model="host.host"
                    label="Host"
                    readonly
                    outlined
                  />
                </v-col>
                <v-col
                  cols="3"
                  md="3"
                >
                  <v-text-field
                    v-model="host.software"
                    label="Software"
                    readonly
                    outlined
                  />
                </v-col>
                <v-col
                  cols="3"
                  md="3"
                >
                  <v-text-field
                    v-model="host.success"
                    label="Success"
                    readonly
                    outlined
                  />
                </v-col>
              </v-row>
              <v-textarea
                style="font: 16px monospace;!important"
                :value="host.output"
                name="input-7-1"
                class="ml-4 mr-4"
                filled
                readonly
                label="Output: "
                auto-grow
              />
            </v-expansion-panel-content>
          </v-expansion-panel>
        </v-expansion-panels>
      </div>
    </v-card>
</div>
</template>


<script>
import XLSX from 'xlsx';
import axios from 'axios'
import snackMessage from '@/api/Error.js'

export default {
  name: 'configure',
  data () {
    return {
      file: "",
      excelFile: "",
      hostToConfigure: [],
      showSummary: false,
      showPassword: false,
      loading: false,
      hosts: [],
      headers:[
        { text: 'Host', align: 'center', value: 'host' },
        { text: 'Port', align: 'center', value: 'port' },
        { text: 'Device Type', align: 'center', value: 'device_type' },
        { text: 'SSH Username', align: 'center', value: 'username' },
        { text: 'Actions',align: 'right', value: 'action', sortable: false },
      ],
      IPorHostname: "",
      software: "",
      username: "",
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
  methods: {
    importExcel(){
       this.excelFile = event.target.files[0];
    },
    pushExcel(){
      XLSX.utils.json_to_sheet(this.hosts, "out.xlsx");
      if (this.excelFile) {
        let fileReader = new FileReader();
        fileReader.readAsBinaryString(this.excelFile);
        fileReader.onload = event => {
          let data = event.target.result;
          let workbook = XLSX.read(data, { type: "binary" });
          workbook.SheetNames.forEach(sheet => {
            let excelArray = XLSX.utils.sheet_to_row_object_array(
              workbook.Sheets[sheet]
            );
            for (const object in excelArray) {
              let excelObject = excelArray[object]
              let keysInObject = Object.keys(excelObject)
              if(excelObject['host'] !== undefined){
                this.pushHost(excelObject['host'], excelObject['port'], excelObject['software'], excelObject['username'], excelObject['password'])
              } else {
                snackMessage("Import Error", 'Missing data in excel.', "red")
              }
            }
          });
        };
      }
    },
    handleFileUpload(event){
      this.file = event
    },
    pushHost(IPorHostname, port, software, username, password){
      if (IPorHostname !== '' && port !== '' && software !== '' && username !== '' && password !== '') {
        if (!this.hostToConfigure.some(hosts => hosts.host === IPorHostname)){
          let data = {
            "host" : IPorHostname,
            "username": username,
            "password": btoa(password),
            "device_type": software, 
            "port": port || 22,
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
        data.append('hosts', hostData)

        axios.post('/webnetter/configure', data, {headers: {'Content-Type': 'multipart/form-data'}})
          .then((response) => {
            if (response.data.status == "success"){
              snackMessage("Success", "Configuration sent", "green")
              this.loading = false
              this.hosts = response.data.data
              this.showSummary = true

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
