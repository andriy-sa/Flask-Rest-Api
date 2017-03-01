import React from 'react'
import {Route, IndexRoute} from 'react-router'
import App from './Components/App'
import Users from './Components/Users'
import Projects from './Components/Projects'
import Login from './Components/Login'
import Project from './Components/Project'
import ProjectEdit from './Components/ProjectEdit'
import requireAuth from './Utils/requireAuth';

export default (
    <Route path='/' component={App}>
        <IndexRoute component={requireAuth(Projects)}/>
      <Route path='/project/:id' component={Project}/>
      <Route path='/project/edit/:id' component={ProjectEdit}/>
        <Route path='/login' component={Login}/>
        <Route path='/users' component={requireAuth(Users)}/>
    </Route>
)

