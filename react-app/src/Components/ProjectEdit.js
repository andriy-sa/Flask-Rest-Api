import React from 'react';
import api from '../Api'
import classNames from 'classnames'
import GettingStartedGoogleMap from "./Blocks/Map"
import RichTextEditor from 'react-rte';


class ProjectEdit extends React.Component {

	constructor(props) {
		super(props);
		this.state = {
			project: {
				title:'',
				description:'',
				price:'',
				published:false
			},
			center: {},
			errors: {},
			editorState: RichTextEditor.createEmptyValue(),
			markers: []
		}
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
				let editorState = RichTextEditor.createValueFromString(response.data.description, 'html')
				this.setState({project: response.data, markers:markers, center:center, editorState:editorState})
			} else {
				this.context.router.push('/404');
			}
		})
	}

	onChangeEditor = (editorState) => {
		let description = editorState.toString('html');
		let project = this.state.project;
		project.description = description
		this.setState({
			editorState,
			project
		});
	};

	handleMapClick = (e) => {
		let project   = this.state.project;
		project.latitude =  e.latLng.lat();
		project.longitude =  e.latLng.lng();

		let markers = [];
		markers.push({
			position: {
				lat: Number(project.latitude),
				lng: Number(project.longitude)
			},
			key: new Date().getTime(),
			defaultAnimation: 1
		});

		this.setState({project:project, markers:markers})
	};

	handleSubmit = (event) => {
		event.preventDefault();
		api.Projects.update(this.state.project)
			.then(response => {
				if (response.status === 200) {
					this.context.router.push('/');
				}
			},
			errors => {
				if(errors.response.status === 404) {
					this.context.router.push('/404');
				}else{
					this.setState({errors: errors.response.data});
				}
			})
	};

	handleChange = (event) => {
		let field    = event.target.name;
		let project   = this.state.project;
		project[field]  = event.target.value;
		this.setState({
			project: project
		});
	};

	handleCheckbox = (event) => {
		let checked = event.target.checked;
		let project   = this.state.project;
		project.published = checked;
		this.setState({
			project: project
		});
	};

	render() {
		return (
			<div id="projectEditPage">
				<div className="page-title">
					Edit Project: <em>{ this.state.project.title}</em>
				</div>
				<form onSubmit={this.handleSubmit}>
					<div className={classNames('form-group',{'has-error': this.state.errors.title})}>
						<label htmlFor="">Title</label>
						<input  onChange={this.handleChange} value={this.state.project.title} name="title" id="title" className="form-control" type="text"/>
						{
							this.state.errors.title &&
							<span className="errors">
									{this.state.errors.title.map((v, i) => {
										return (<span key={i} className="help-block">{v}</span>)
									})}
								</span>
						}
					</div>
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
						onMapClick={this.handleMapClick.bind(this)}
						center={this.state.center}
					/>
					}
					<div className="form-group">
						<label htmlFor="">Description</label>
						<RichTextEditor
							value={this.state.editorState}
							onChange={this.onChangeEditor}
						/>
					</div>
					<div className={classNames('form-group',{'has-error': this.state.errors.price})}>
						<label htmlFor="">Price</label>
						<input  onChange={this.handleChange} value={this.state.project.price} name="price" id="price" className="form-control" type="number"/>
						{
							this.state.errors.price &&
								<span className="errors">
									{this.state.errors.price.map((v, i) => {
										return (<span key={i} className="help-block">{v}</span>)
									})}
								</span>
						}
					</div>
					<div className='form-group'>
						<label htmlFor="published">
							<input onChange={this.handleCheckbox} checked={this.state.project.published} value='1' name="published" id="published" type="checkbox"/>
							<span>Published</span>
						</label>
					</div>
					<button className="btn btn-primary">Save</button>
				</form>
			</div>
		)
	}
}

ProjectEdit.contextTypes = {
	router: React.PropTypes.object.isRequired
};

export default ProjectEdit;