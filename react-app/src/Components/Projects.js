import React from 'react';
import api from '../Api'

class Projects extends React.Component {

  state = {
    projects: []
  }

  componentWillMount() {
    api.Projects.search().then(response => {
      if (response.status === 200) {
        this.setState({projects: response.data.hits})
      } else {
        this.setState({projects: []})
      }
    })
  }

  render() {
    return (
      <div className="projects">
        <h>Projects List:</h>
        <p className="App-intro">
          {this.state.projects.map((v, i) => {
            return <li key={i}>{v._source.title}</li>
          })}
        </p>
      </div>
    );
  }
}

export default Projects;