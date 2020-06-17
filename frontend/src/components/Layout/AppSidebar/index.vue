<template>
  <v-navigation-drawer
    v-model="cMenu"
    :mini-variant.sync="cMini"
    mini-variant-width="57"
    app
    dark
  >
    <v-row>
      <v-col 
        cols="12"
        class="text-center"
      >
        <transition
          name="fade"
          style="transition-delay:151s"
        >
          <div
            v-if="!mini" 
            style="cursor: pointer;"
            class="white--text title text-center"
            @click="$router.push({name:'home'})"
          >
            WebNetter API
          </div>
        </transition>
      </v-col>
    </v-row>
    <v-divider 
      v-if="!mini"
    />
    <div
      v-if="!mini" 
      class="white--text heading text-center fwl"
    >
      <b>Version:</b> 1.0
    </div>
    <v-divider 
      v-if="!mini"
    />
    <v-list dense>
      <span 
        v-for="item in items"
        :key="item.text"
      >
        <v-list-item
          v-if="!item.subItems.length"
          :to="item.route"
        >
          <v-list-item-action>
            <v-tooltip bottom>
              <template v-slot:activator="{ on }">
                <v-icon v-on="on">{{ item.icon }}</v-icon>
              </template>
              <span>{{ item.text }}</span>
            </v-tooltip>
          </v-list-item-action>
          <v-list-item-content>
            <v-list-item-title>
              {{ item.text }}
            </v-list-item-title>
          </v-list-item-content>
        </v-list-item>
        <v-list-group
          v-else
          :key="item.title"
          v-model="item.active"
          no-action
          class="ma-0 pa-0"
        >
          <template 
            v-slot:activator
            @click.prevent
          >
            <v-list-item-action 
              @click.prevent
            >
              <v-tooltip
                bottom 
                @click.prevent
              >
                <template
                  v-slot:activator="{ on }" 
                  @click.prevent
                >
                  <v-icon v-on="on">{{ item.icon }}</v-icon>
                </template>
                <span>{{ item.text }}</span>
              </v-tooltip>
            </v-list-item-action>
            <v-list-item-content>
              <v-list-item-title>
                {{ item.text }}
              </v-list-item-title>
            </v-list-item-content>
          </template>

          <v-list-item
            v-for="subItem in item.subItems"
            :key="subItem.title"
            :to="subItem.route"
            active-class="white--text"
          >
            <v-list-item-content>
              <v-list-item-title v-text="subItem.text" />
            </v-list-item-content>
          </v-list-item>
        </v-list-group>
      </span>
    </v-list>
  </v-navigation-drawer>
</template>
<script>
export default {
  name: 'AppSidebar',
  props: {
    showOnlyLogo: {
      type: Boolean,
      default: false
    },
  },
  data() {
    return {
      menu: true,
      mini: false,
      currentIPaddress: '',
      showTitle: false
    }
  },
  computed: {
    cMenu: {
      // getter
      get () {
        return this.menu
      },
      // setter
      set (nV) {
        this.menu = nV
        return this.$emit('showOnlyLogo', nV)
      }
    },
    cMini: {
      // getter
      get () {
        return this.mini
      },
      // setter
      set (nV) {
        this.mini = nV
      }
    },
    items () {
      return [
        { subItems: [], icon: 'fa-home', text: 'Home' , route: {name: 'home'}},
        { subItems: [], icon: 'fa-server', text: 'Webnetter API' , route: {name: 'webnetter'}}
      ]
    },
  },
  watch: {
    showOnlyLogo: {
      immediate: true,
      handler: function (newValue) {
        this.menu = newValue
      }
    }
  }
}
</script>

<style>
.fade-enter-active {
  transition: opacity 1s;
}
.fade-leave-active {
  transition: opacity 1s;
}
.fade-enter, .fade-leave-to {
  opacity: 0;
}
.center {
  margin: auto;
  width: 50%;
}
</style>
