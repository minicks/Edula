import axios from 'axios';
import { BASE_URL, setToken } from './utils';

export const apiGetFriendList = () =>
	axios({
		method: 'get',
		url: `${BASE_URL}/accounts/friend/`,
		headers: {
			...setToken(),
		},
	});

export const apiDeleteFriend = (friendId: string) =>
	axios({
		method: 'delete',
		url: `${BASE_URL}/accounts/friend/${friendId}/`,
		headers: {
			...setToken(),
		},
	});

export const apiGetFriendRequestList = () =>
	axios({
		method: 'get',
		url: `${BASE_URL}/accounts/friend/request/`,
		headers: {
			...setToken(),
		},
	});

export const apiPostFriendRequest = (friendId: string) =>
	axios({
		method: 'post',
		url: `${BASE_URL}/accounts/friend/request/`,
		headers: {
			...setToken(),
		},
		data: {
			toUser: friendId,
		},
	});

export const apiPutFriendRequest = (requestId: string, requestStatus: string) =>
	axios({
		method: 'put',
		url: `${BASE_URL}/accounts/friend/request/${requestId}/`,
		headers: {
			...setToken(),
		},
		data: {
			requestStatus,
		},
	});

export const apiDeleteFriendRequest = (requestId: string) =>
	axios({
		method: 'delete',
		url: `${BASE_URL}/accounts/friend/request/${requestId}/`,
		headers: {
			...setToken(),
		},
	});

export const apigetSearchFriend = (keyword: string) =>
	axios({
		method: 'get',
		url: `${BASE_URL}/accounts/friend/search/${keyword}/`,
		headers: {
			...setToken(),
		},
	});
