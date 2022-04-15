<template>
  <v-data-table
    :headers="headers"
    :items="items"
    sort-by="host"
    class="elevation-1"
  >
    <template top>
    </template>
    <template v-slot:[`item.action`]="{ item }">
        <v-dialog v-model="dialog" max-width="500px">
          <v-card>
            <v-card-title>
              <span class="headline">Edit Item</span>
            </v-card-title>

            <v-card-text>
              <v-container>
                <v-row>
                  <v-col cols="12" sm="8" md="8">
                    <v-text-field outlined v-model="editedItem.host" label="IP address/ Hostname"></v-text-field>
                  </v-col>
                  <v-col cols="12" sm="4" md="4">
                    <v-text-field outlined v-model="editedItem.port" label="SSH Port"></v-text-field>
                  </v-col>
                  <v-col cols="12" sm="12" md="12">
                    <v-select
                      v-model="editedItem.device_type"
                      :items="diffrentSoftware"
                      label="Software on host"
                      outlined
                    />
                  </v-col>
                  <v-col cols="12" sm="6" md="6">
                    <v-text-field outlined v-model="editedItem.username" label="SSH Username"></v-text-field>
                  </v-col>
                  <v-col cols="12" sm="6" md="6">
                    <v-text-field outlined type="password" v-model="editedItem.password" label="SSH Password"></v-text-field>
                  </v-col>
                  <v-col cols="12" sm="12" md="12">
                    <v-text-field outlined v-if="holder.command" v-model="editedItem.command" label="Command to run"></v-text-field>
                  </v-col>
                  <v-col cols="12" sm="12" md="12">
                    <v-text-field outlined v-if="holder.location" v-model="editedItem.location" label="File Location"></v-text-field>
                  </v-col>
                </v-row>
              </v-container>
            </v-card-text>

            <v-card-actions>
              <v-spacer></v-spacer>
              <v-btn color="blue darken-1" text @click="close">Cancel</v-btn>
              <v-btn color="blue darken-1" text @click="save">Save</v-btn>
            </v-card-actions>
          </v-card>
          <template v-slot:activator="{ on }">
          <v-icon
            small
            class="mr-2"
            @click="editItem(item)"
            v-on="on"
          >
            edit
          </v-icon>
          </template>
        </v-dialog>
        <v-icon
          small
          @click="deleteItem(item)"
        >
          delete
        </v-icon>
    </template>
    <template slot="no-data">
      <v-card-text> {{ emptyText }}</v-card-text>
    </template>
  </v-data-table>
</template>

<script>
  export default {
    data: () => ({
      dialog: false,
      editedIndex: -1,
      editedItem: {
        host: '',
        username: '',
        password: '',
        device_type: '',
        location: '',
        port: '',
        command: ''
      },
      defaultItem: {
        host: '',
        username: '',
        password: '',
        device_type: '',
        location: '',
        port: '',
        command: ''
      },
      holder: {
        location: false,
        command: false,
      },
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
    }),
    props: {
      items: {
        type: [Array],
        default: function () {
          return []
        }
      },
      emptyText: {
        type: String,
        default: function (){
          return ''
        }
      },
      headers: {
        type: [Array],
        default: function () {
          return []
        }
      },
    },
    watch: {
      dialog (val) {
        val || this.close()
      },
    },
    methods: {
      editItem (item) {
        for (const i in this.headers) {
          let valName = this.headers[i].value
          if (valName == 'location'){this.holder.location = true}
          if (valName == 'command'){this.holder.command = true}
        }
        this.editedIndex = this.items.indexOf(item)
        this.editedItem = Object.assign({}, item)
        this.defaultItem = Object.assign({}, item)
        this.dialog = true
      },

      deleteItem (item) {
        let items_data = this.items;
        const index = items_data.indexOf(item)
        confirm('Are you sure you want to delete this item?') && items_data.splice(index, 1) && this.$emit("update-items", items_data);
      },

      close () {
        this.dialog = false
        setTimeout(() => {
          this.editedItem = Object.assign({}, this.defaultItem)
          this.editedIndex = -1
        }, 300)
      },

      save () {
        if (this.editedIndex > -1) {
          let items_data = this.items;
          Object.assign(items_data[this.editedIndex], this.editedItem)
          this.$emit("update-items", items_data);
        } else {
          let items_data = this.items;
          items_data.push(this.editedItem)
          this.$emit("update-items", items_data);
        }
        this.close()
      },
    },
  }
</script>