import React from 'react'
import {Link} from 'react-router'
import classNames from 'classnames'
import {connect} from 'react-redux'
import {setUser} from '../../Actions/Auth'

class Header extends React.Component {

  logout = () => {
    localStorage.setItem('jwtToken', '');
    this.props.setUser(null);
    this.context.router.push('/login');
  };

  render() {

    return (<div className="header">
      <nav className="navbar navbar-default m-b-0">
        <div className="container">
          <div className="navbar-header">
            <button type="button" className="navbar-toggle collapsed" data-toggle="collapse"
                    data-target="#bs-example-navbar-collapse-1" aria-expanded="false">
              <span className="sr-only">Toggle navigation</span>
              <span className="icon-bar"></span>
              <span className="icon-bar"></span>
              <span className="icon-bar"></span>
            </button>
            <Link className="navbar-brand" to='/'>Brand</Link>
          </div>
          <div className="collapse navbar-collapse" id="bs-example-navbar-collapse-1">
            <ul className="nav navbar-nav">
              <li className={classNames({'active': this.props.path === '/'})}><Link to='/'>Projects</Link></li>
              <li className={classNames({'active': this.props.path === '/users'})}><Link to='/users'>Users</Link></li>
            </ul>

            {this.props.user ? (
              <ul className="nav navbar-nav navbar-right">
                <li className='profile-link'><Link to='/'>Profile ({this.props.user.username})</Link></li>
                <li className='logout-link'><a onClick={this.logout} href="#">Logout</a></li>
              </ul>
            ) : (
              <ul className="nav navbar-nav navbar-right">
                <li className='login-link'><Link to='/login'>Login</Link></li>
              </ul>
            )}
          </div>
        </div>
      </nav>
    </div>)
  }
}

Header.contextTypes = {
  router: React.PropTypes.object.isRequired
};

Header.propTypes = {
  setUser: React.PropTypes.func.isRequired
};

export default connect(null, {setUser})(Header)