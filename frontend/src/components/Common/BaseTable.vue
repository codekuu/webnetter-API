<template>
  <v-data-table
    :headers="headers"
    :items="items"
    sort-by="host"
    class="elevation-1"
  >
    <template v-slot:top>
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
                  <v-col cols="12" sm="6" md="6">
                    <v-text-field outlined v-model="editedItem.username" label="SSH Username"></v-text-field>
                  </v-col>
                  <v-col cols="12" sm="6" md="6">
                    <v-text-field outlined type="password" v-model="editedItem.password" label="SSH Password"></v-text-field>
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
        </v-dialog>
    </template>
    <template v-slot:item.action="{ item }">
      <v-icon
        small
        class="mr-2"
        @click="editItem(item)"
      >
        edit
      </v-icon>
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
        device_type: '',
        port: '',
      },
      defaultItem: {
        host: '',
        username: '',
        device_type: '',
        port: '',
      },
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
        this.editedIndex = this.items.indexOf(item)
        this.editedItem = Object.assign({}, item)
        this.dialog = true
      },

      deleteItem (item) {
        const index = this.items.indexOf(item)
        confirm('Are you sure you want to delete this item?') && this.items.splice(index, 1)
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
          Object.assign(this.items[this.editedIndex], this.editedItem)
        } else {
          this.items.push(this.editedItem)
        }
        this.close()
      },
    },
  }
</script>