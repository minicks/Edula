import styled from 'styled-components';
import OpenViduVideoComponent from './OvVideo';

function UserVideoComponent({ streamManager }) {
	const getNicknameTag = () =>
		JSON.parse(streamManager.stream.connection.data).clientData;

	return streamManager !== undefined ? (
		<>
			<OpenViduVideoComponent streamManager={streamManager} />
			<div>{getNicknameTag()}</div>
		</>
	) : null;
}

export default UserVideoComponent;
