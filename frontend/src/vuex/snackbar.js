// import Vue from 'vue'

export default {
  state: {
    snackShow: false,
    snackColor: 'primary',
    snackMessage: '',
    snackTitle: '',
    snackTimeoutID: '',
    snackTimeout: 7000,
    snackUndoCallback: []
  },
  mutations: {
    snack(state, payload) {
      if (payload.timeout) {
        state.snackTimeout = payload.timeout
      }
      setTimeout(() => {
        state.snackShow = false
      }, payload.timeout)
      state.snackTitle = payload.title
      state.snackMessage = payload.message
      state.snackColor = payload.color
      state.snackShow = payload.show
      if (payload.hasOwnProperty('undoCallback')) {
        state.snackUndoCallback = payload.undoCallback
      } else {
        state.snackUndoCallback = []
      }
    },
    snackShow(state, payload) {
      state.snackShow = payload
    },
    snackTimeoutID(state, payload) {
      state.snackTimeoutID = payload
    },
  },
  getters: {
    snackShow: state => state.snackShow,
    snackColor: state => state.snackColor,
    snackMessage: state => state.snackMessage,
    snackTitle: state => state.snackTitle,
    snackTimeout: state => state.snackTimeout,
    snackUndoCallback: state => state.snackUndoCallback,
    snackUndoLength: state => state.snackUndoCallback.length,
  },
  actions: {
    snack({ commit }, payload) {
      // close previous snackbar
      commit('snackShow', false)
      commit('snack', payload)
    },
    // snack Undo
    snackUndoCallback({state}) {
      if (state.snackUndoCallback.length) {
        console.log('Snack undo action')
        // Vue.prototype.$API.func()
      }
    }
  }
}
