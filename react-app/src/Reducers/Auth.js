import { SET_USER } from '../Actions/Auth'

const initialState = {
  activeUser: null
};

export default (state = initialState, action = {}) => {

  switch (action.type) {

    case SET_USER:
      return Object.assign({}, {activeUser: action.activeUser})

    default:
      return state
  }
}