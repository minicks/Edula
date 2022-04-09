import axios from 'axios';
import { BASE_URL, setToken } from './utils';

export const apiSignup = (
	firstName: string,
	password: string,
	schoolName: string,
	schoolAbb: string
) =>
	axios({
		method: 'post',
		url: `${BASE_URL}/accounts/resister/`,
		data: {
			firstName,
			password,
			school: {
				name: schoolName,
				abbreviation: schoolAbb,
			},
		},
	});

export const apiGetAdmin = (schoolAdminPk: string) =>
	axios({
		method: 'get',
		url: `${BASE_URL}/accounts/school-admin/${schoolAdminPk}/`,
		headers: {
			...setToken(),
		},
	});

export const apiCreateUsers = (data: object) =>
	axios({
		method: 'post',
		url: `${BASE_URL}/accounts/user/`,
		headers: {
			...setToken(),
		},
		data,
	});

export const apiDeleteUsers = (year: string) =>
	axios({
		method: 'delete',
		url: `${BASE_URL}/accounts/user/Y/${year}/`,
		headers: {
			...setToken(),
		},
	});

export const apiDeleteUser = (studentId: string) =>
	axios({
		method: 'delete',
		url: `${BASE_URL}/accounts/user/S/${studentId}/`,
		headers: {
			...setToken(),
		},
	});

export const apiPutUser = (userId: number, user: object) =>
	axios({
		method: 'put',
		url: `${BASE_URL}/accounts/user/`,
		headers: {
			...setToken(),
		},
		data: {
			user: userId,
			...user,
		},
	});
