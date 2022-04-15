import Vue from 'vue'
import Vuetify from 'vuetify/lib'

import colors from 'vuetify/lib/util/colors'
Vue.use(Vuetify)

export default new Vuetify({
  icons: {
    iconfont: 'mdi'
  },
  theme: {
    themes: {
      light: {
        primary: "#0082bf", // #0082bf
        secondary: "#0082bf", // #0082bf
        warning: colors.orange.darken3, // #3F51B5
        accent: colors.indigo.base, // #3F51B5
      },
      dark: {
        primary: "#0082bf", // #0082bf
        secondary: "#0082bf", // #0082bf
        accent: colors.indigo.base, // #3F51B5
        warning: colors.orange.darken3, // #3F51B5
      },
    },
  },
})
