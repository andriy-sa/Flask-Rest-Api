import React from 'react';
import Header from './Blocks/Header'

class App extends React.Component {

  state = {
    activeUser: null
  }

  logout() {
    localStorage.setItem('jwtToken', '');
    this.setState({
      activeUser: null
    });
    this.context.router.push('/login');
  };


  render() {
    let path = this.props.location.pathname;
    return (
      <div className="App">
        <Header path={path} user={this.state.activeUser}/>
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
