import React from 'react';
import Header from './Blocks/Header'
import { connect } from 'react-redux'

class App extends React.Component {

  render() {
    let path = this.props.location.pathname;
    return (
      <div className="App">
        <Header path={path} user={this.props.activeUser}/>
        <div id="content">
          <div className="container">
            {this.props.children}
          </div>
        </div>
      </div>
    );
  }
}

function mapStateToProps(state) {
  return {
    activeUser: state.authReducer.activeUser
  }
}

export default connect(mapStateToProps, {})(App);
