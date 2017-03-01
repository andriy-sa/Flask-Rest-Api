import React from 'react';
import { withGoogleMap, GoogleMap, Marker } from "react-google-maps";
import withScriptjs from "react-google-maps/lib/async/withScriptjs";


const Map = ({project, markers}) => {
	let GettingStartedGoogleMap = withScriptjs( withGoogleMap(props => (
		<GoogleMap
			ref={props.onMapLoad}
			defaultZoom={17}
			defaultCenter={{ lat: Number(props.project.latitude), lng: Number(props.project.longitude) }}>
			{props.markers.map((marker, index) => (
				<Marker
					{...marker}
				/>
			))}
		</GoogleMap>
	)));

	let mapObject = (
		<GettingStartedGoogleMap
			googleMapURL="https://maps.googleapis.com/maps/api/js?v=3.exp"
			loadingElement={
				<div style={{ height: `400px` }}>
					Loading...
				</div>
			}
			containerElement={
				<div style={{ height: `400px` }} />
			}
			mapElement={
				<div style={{ height: `400px` }} />
			}
			project={project}
			markers={markers}
		/>
	);

	return project ? mapObject : null
};

export default Map