import React from 'react';
import ReactDOM from 'react-dom';
import { Router, browserHistory} from 'react-router'
import routes from './Routes'
import { Provider } from 'react-redux'
import rootReducer from './rootReducer'
import thunk from 'redux-thunk'
import { createStore, applyMiddleware } from 'redux'
import { composeWithDevTools } from 'redux-devtools-extension'

let store = createStore(rootReducer, composeWithDevTools(applyMiddleware(thunk)))

ReactDOM.render(
  <Provider store={store}>
    <Router history={browserHistory} routes={routes} />
  </Provider>,
  document.getElementById('root')
);
