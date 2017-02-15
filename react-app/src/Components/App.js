import React from 'react';
import {Link} from 'react-router'
import classNames from 'classnames'
import api from '../Api'

class App extends React.Component {

  state = {
    activeUser: null
  }
  componentWillMount() {
    this.check_me()
    api.Auth.force_login().then(response => {})
  }

  componentWillReceiveProps() {
    this.check_me()
  }

  check_me(){
    api.Auth.me().then(response => {
      this.setState({activeUser: response.data})
    }).catch(e => {
      this.setState({activeUser: null})
    })
  }

    render() {
        const path = this.props.location.pathname;
        return (
            <div className="App">
                <div className="header">
                  <nav className="navbar navbar-default">
                    <div className="container">
                      <div className="navbar-header">
                        <button type="button" className="navbar-toggle collapsed" data-toggle="collapse" data-target="#bs-example-navbar-collapse-1" aria-expanded="false">
                          <span className="sr-only">Toggle navigation</span>
                          <span className="icon-bar"></span>
                          <span className="icon-bar"></span>
                          <span className="icon-bar"></span>
                        </button>
                        <Link className="navbar-brand"  to='/'>Brand</Link>
                      </div>
                      <div className="collapse navbar-collapse" id="bs-example-navbar-collapse-1">
                        <ul className="nav navbar-nav">
                          <li className={classNames({'active': path === '/'})}><Link to='/'>Projects</Link></li>
                          <li className={classNames({'active': path === '/users'})}><Link  to='/users'>Users</Link></li>
                        </ul>
                      </div>
                    </div>
                  </nav>
                </div>
                <div id="content">
                  <div className="container">
                    {this.props.children}
                  </div>
                </div>
            </div>
        );
    }
}

export default App;
