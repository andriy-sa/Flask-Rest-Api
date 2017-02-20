import React from 'react';
import {connect} from 'react-redux';
import api from '../Api'
import { setUser } from '../Actions/Auth'

export default function (ComposedComponent) {
  class Authenticate extends React.Component {

    //constructor(props){
    //  super(props);
    //
    //  this.state = {
    //    activeUser: null
    //  }
    //}

    componentWillMount() {
      this.checkLogin()
    }

    checkLogin = () => {
      api.Auth.me().then(response => {
        this.props.setUser(response.data)
      }).catch(e => {
        this.props.setUser(null);
        this.context.router.push('/login');
      })
    };

    render() {
      if (!this.props.activeUser) {
        return false
      }

      return (
        <ComposedComponent  {...this.props} />
      );
    }
  }

  Authenticate.contextTypes = {
    router: React.PropTypes.object.isRequired
  };

  Authenticate.propTypes = {
    setUser: React.PropTypes.func.isRequired
  };

  function mapStateToProps(state) {
    return {
      activeUser: state.authReducer.activeUser
    }
  }

  return connect(mapStateToProps, {setUser})(Authenticate);
}