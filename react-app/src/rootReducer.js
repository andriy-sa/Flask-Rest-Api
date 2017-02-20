import { combineReducers } from 'redux'
import appReducer from './Reducers/App'
import authReducer from  './Reducers/Auth'

export default combineReducers({
  appReducer,
  authReducer
})