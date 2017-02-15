import React from 'react'
import {Route, IndexRoute} from 'react-router'
import App from './Components/App'
import Users from './Components/Users'
import Projects from './Components/Projects'

export default (
    <Route path='/' component={App}>
        <IndexRoute component={Projects}/>
        <Route path='/users' component={Users}/>
    </Route>
)

