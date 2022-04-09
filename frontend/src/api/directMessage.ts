import axios from 'axios';
import { BASE_URL, setToken } from './utils';

export const apiGetMessages = (
	userPk: string,
	page: string,
	pageSize: string
) =>
	axios({
		method: 'get',
		url: `${BASE_URL}/messages/${userPk}?page=${page}&page_size=${pageSize}`,
		headers: {
			...setToken(),
		},
	});

export const apiGetMessageCnt = () =>
	axios({
		method: 'get',
		url: `${BASE_URL}/messages/count/`,
		headers: {
			...setToken(),
		},
	});

export const apiGetUserMessageCnt = (userPk: string) =>
	axios({
		method: 'get',
		url: `${BASE_URL}/messages/count/${userPk}/`,
		headers: {
			...setToken(),
		},
	});

export const apiPostMessage = (userPk: string, content: string) =>
	axios({
		method: 'post',
		url: `${BASE_URL}/messages/${userPk}/`,
		headers: {
			...setToken(),
		},
		data: {
			content,
		},
	});

export const apiPatchMessage = (userPk: string, messagePk: string) =>
	axios({
		method: 'patch',
		url: `${BASE_URL}/messages/${userPk}/${messagePk}/`,
		headers: {
			...setToken(),
		},
	});
export const apiDeleteMessage = (userPk: string, messagePk: string) =>
	axios({
		method: 'delete',
		url: `${BASE_URL}/messages/${userPk}/${messagePk}/`,
		headers: {
			...setToken(),
		},
	});
