export const BASE_URL = `${process.env.REACT_APP_PROTOCOL}://${window.location.hostname}:${process.env.REACT_APP_PORT}/api`;
export const OPENVIDU_SERVER_URL = `https://${window.location.hostname}:${process.env.REACT_APP_OPENVIDU_PORT}`;
export const OPENVIDU_SERVER_SECRET = 'MY_SECRET';

export const setToken = () => {
	const token = localStorage.getItem('access') || ``;
	const config = {
		Authorization: `JWT ${token}`,
	};
	return config;
};
