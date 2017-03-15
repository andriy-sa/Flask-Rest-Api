import React from 'react';
import api from '../Api'
import Map from './Blocks/Map'

class Project extends React.Component {

	constructor(props) {
		super(props);
		this.state = {
			project: {},
			markers: []
		}
	};

	createMarkup = (data) => {
		return {__html: data}
	};

	componentDidMount() {
		let id = this.props.params.id || 0;
		api.Projects.get_by_id(id).then(response => {
			if (response.status === 200) {
				let markers = [];
				markers.push({
					position: {
						lat: Number(response.data.latitude),
						lng: Number(response.data.longitude)
					},
					key: new Date().getTime(),
					defaultAnimation: 2
				});
				this.setState({project: response.data, markers: markers})
			} else {
				this.context.router.push('/404');
			}
		})
	}

	render() {
		return (
			<div id="projectPage">
				<div className="col-sm-6">
					<div className="project-title">
						{ this.state.project.title }
					</div>
					<div className="price">
						<label>Price:</label>
						<span>${ this.state.project.price }</span>
					</div>
					<div dangerouslySetInnerHTML={this.createMarkup(this.state.project.description)}
							 className="project-description">
					</div>
					<div className="project-date">
						<label>Date:</label>
						<span>{ this.state.project.created_at }</span>
					</div>
				</div>
				<div className="col-sm-6">
					<div className="project-map">
						<Map project={this.state.project} markers={this.state.markers}/>
					</div>
				</div>
			</div>
		)
	}
}

Project.contextTypes = {
	router: React.PropTypes.object.isRequired
};

export default Project;