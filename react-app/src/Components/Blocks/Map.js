import React from 'react';
import {withGoogleMap, GoogleMap, Marker} from "react-google-maps";
import withScriptjs from "react-google-maps/lib/async/withScriptjs";

const GettingStartedGoogleMap = withScriptjs(withGoogleMap(props => (
	<GoogleMap
		ref={props.onMapLoad}
		defaultZoom={17}
		onClick={props.onMapClick ? props.onMapClick : ()=>{} }
		defaultCenter={props.center}>
		{props.markers.map((marker, index) => (
			<Marker
				{...marker}
			/>
		))}
	</GoogleMap>
)));

export default GettingStartedGoogleMap