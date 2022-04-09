import axios, { AxiosError } from 'axios';
import { OPENVIDU_SERVER_URL, OPENVIDU_SERVER_SECRET } from './utils';

export const createSession = async (sessionId: string) => {
	const data = JSON.stringify({ customSessionId: sessionId });
	try {
		const response = await axios.post(
			`${OPENVIDU_SERVER_URL}/openvidu/api/sessions`,
			data,
			{
				headers: {
					Authorization: `Basic ${btoa(`OPENVIDUAPP:${OPENVIDU_SERVER_SECRET}`)}`,
					'Content-Type': 'application/json',
				},
			}
		);
		console.log('CREATE SESSION', response);
		return response.data.id;
	} catch (e: any) {
		const error = e as AxiosError;
		if (error?.response?.status === 409) {
			return sessionId;
		}
		console.log(error);
		console.warn(
			`No connection to OpenVidu Server. This may be a certificate error at ${OPENVIDU_SERVER_URL}`
		);
		if (
			window.confirm(
				`No connection to OpenVidu Server. This may be a certificate error at "${OPENVIDU_SERVER_URL}"\n\nClick OK to navigate and accept it. ` +
					`If no certificate warning is shown, then check that your OpenVidu Server is up and running at "${OPENVIDU_SERVER_URL}"`
			)
		) {
			window.location.assign(`${OPENVIDU_SERVER_URL}/openvidu/accept-certificate`);
		}
		return new Error(e);
	}
};

export const createToken = async (sessionId: string) => {
	const data = {};
	try {
		const response = await axios.post(
			`${OPENVIDU_SERVER_URL}/openvidu/api/sessions/${sessionId}/connection`,
			data,
			{
				headers: {
					Authorization: `Basic ${btoa(`OPENVIDUAPP:${OPENVIDU_SERVER_SECRET}`)}`,
					'Content-Type': 'application/json',
				},
			}
		);
		console.log('TOKEN', response);
		return response.data.token;
	} catch (e: any) {
		throw new Error(e);
	}
};
