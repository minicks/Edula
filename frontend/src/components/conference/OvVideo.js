/* eslint-disable jsx-a11y/media-has-caption */
import { createRef, useEffect } from 'react';
import styled from 'styled-components';

function OpenVideoComponent({ streamManager }) {
	const videoRef = createRef();

	useEffect(() => {
		if (streamManager && !!videoRef) {
			streamManager.addVideoElement(videoRef.current);
		}
	}, [streamManager]);

	return <video autoPlay ref={videoRef} />;
}

export default OpenVideoComponent;
