import React from 'react'
import {Link} from 'react-router'
import classNames from 'classnames'

const Header = ({path, user}) => {

  return (
    <div className="header">
      <nav className="navbar navbar-default">
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
              <li className={classNames({'active': path === '/'})}><Link to='/'>Projects</Link></li>
              <li className={classNames({'active': path === '/users'})}><Link to='/users'>Users</Link></li>
            </ul>

            {user ? (
              <ul className="nav navbar-nav navbar-right">
                <li className='profile-link'><Link to='/'>Profile</Link></li>
                <li className='logout-link'><a href="#">Logout</a></li>
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

export default Header