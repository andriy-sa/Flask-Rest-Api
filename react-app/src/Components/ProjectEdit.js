import React from 'react';
import api from '../Api'

class ProjectEdit extends React.Component {

	constructor(props) {
		super(props);
		this.state = {
			project: {},
			markers: []
		}
	};

	componentDidMount(){
		let id = this.props.params.id || 0;
		api.Projects.get_by_id(id).then(response => {
			if (response.status === 200) {
				this.setState({project : response.data})
			}else{
				this.context.router.push('/404');
			}
		})
	}

	render() {
		return (
			<div id="projectPage">
				Edit Project: <em>{ this.state.project.title}</em>
			</div>
		)
	}
}

ProjectEdit.contextTypes = {
	router: React.PropTypes.object.isRequired
};

export default ProjectEdit;