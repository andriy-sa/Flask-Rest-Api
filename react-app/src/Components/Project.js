import React from 'react';
import api from '../Api'
import GettingStartedGoogleMap from "./Blocks/Map"
import {Link} from 'react-router'

class Project extends React.Component {

	constructor(props) {
		super(props);
		this.state = {
			project: {},
			markers: [],
			center: {}
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
				let center = {
					lat: Number(response.data.latitude),
					lng: Number(response.data.longitude)
				};
				this.setState({project: response.data, markers: markers, center:center})
			} else {
				this.context.router.push('/404');
			}
		})
	}

	render() {
		return (
			<div id="projectPage">
				<div className="col-sm-6">
					<Link className='btn btn-success' to={`/project/edit/${this.state.project.id}`}>
						Edit
					</Link>
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
						{this.state.project.latitude &&
							<GettingStartedGoogleMap
								googleMapURL="https://maps.googleapis.com/maps/api/js?v=3.exp"
								loadingElement={
									<div style={{height: `400px`}}>
										Loading...
									</div>
								}
								containerElement={
									<div style={{height: `400px`}}/>
								}
								mapElement={
									<div style={{height: `400px`}}/>
								}
								project={this.state.project}
								markers={this.state.markers}
								center={this.state.center}
							/>
						}
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