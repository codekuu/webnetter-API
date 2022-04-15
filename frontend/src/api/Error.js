import store from '../vuex'

function error (title, message, color) {
  const snack = { 
    show: true,
    color: color,
    timeout: 7000,
    title: title,
    message: message
  }
  store.commit('snack', snack)
}


export default error