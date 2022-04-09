import axios from 'axios';
import { BASE_URL, setToken } from './utils';

export const apiGetNotifications = (page: string, pageSize: string) =>
	axios({
		method: 'get',
		url: `${BASE_URL}/notifications?page=${page}&page_size=${pageSize}`,
		headers: {
			...setToken(),
		},
	});

export const apiPatchNotification = (notificationPk: string) =>
	axios({
		method: 'patch',
		url: `${BASE_URL}/notifications/${notificationPk}/`,
		headers: {
			...setToken(),
		},
	});

export const apiDeleteNotification = (notificationPk: string) =>
	axios({
		method: 'delete',
		url: `${BASE_URL}/notifications/${notificationPk}/`,
		headers: {
			...setToken(),
		},
	});

export const apiGetNotificationCnt = () =>
	axios({
		method: 'get',
		url: `${BASE_URL}/notifications/count/`,
		headers: {
			...setToken(),
		},
	});

export const apiGetTotalNotificationCnt = () =>
	axios({
		method: 'get',
		url: `${BASE_URL}/notifications/count/all/`,
		headers: {
			...setToken(),
		},
	});
