import React from 'react'
import Api from '../Api'
import axios from 'axios'

class Login extends React.Component {

  constructor(props) {
    super(props);

    this.state = {
      user: {
        'email': '',
        'password': ''
      },
      error: ''
    }
  }

  onChange = event => {
    const field = event.target.name;
    const user = this.state.user;
    user[field] = event.target.value;
    this.setState({
      user: user
    });
  };

  login = () => {
    const user = this.state.user;
    const thisClass = this;
    Api.Auth.login(user)
    .then(response => {
      thisClass.setState({
        error: ''
      });
      localStorage.setItem('jwtToken', response.data.access_token);
      axios.defaults.headers.common['Authorization'] = `JWT ${response.data.access_token}`;

    }, (e) => {
      if (e.response && e.response.data && e.response.data.description) {
        thisClass.setState({
          error: e.response.data.description
        });
      }
    })
  };

  render() {
    return (
      <div className="App">
        <div className="panel panel-default">
          <div className="panel-heading">Login</div>
          <div className="panel-body">
            {this.state.error &&
            <div className="alert alert-danger" role="alert"> { this.state.error } </div>
            }
            <div className="form-group">
              <label>Email</label>
              <input className="form-control" onChange={this.onChange} value={this.state.user.email} type="text"
                     name="email"/>
            </div>
            <div className="form-group">
              <label>Password</label>
              <input className="form-control" onChange={this.onChange} value={this.state.user.password} type="password"
                     name="password"/>
            </div>
            <button onClick={this.login} className="btn btn-primary">Login</button>
          </div>
        </div>
      </div>
    );
  }
}
export default Login