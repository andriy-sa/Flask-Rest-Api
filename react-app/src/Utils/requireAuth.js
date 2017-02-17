import React from 'react';
import { connect } from 'react-redux';
import api from '../Api'

export default function (ComposedComponent) {
  class Authenticate extends React.Component {
    componentWillMount() {
      this.checkLogin()
    }

    checkLogin = () => {
      api.Auth.me().then(response => {
        // this.setState({activeUser: response.data})
      }).catch(e => {
        console.log(e);
        this.context.router.push('/login');
      })
    };

    render() {
      return (
        <ComposedComponent  {...this.props} />
      );
    }
  }

  Authenticate.contextTypes = {
    router: React.PropTypes.object.isRequired
  }


  return Authenticate;
}