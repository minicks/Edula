import axios from 'axios';
import { BASE_URL, setToken } from './utils';

export const apiLogin = (userId: string, password: string) =>
	axios({
		method: 'post',
		url: `${BASE_URL}/token/`,
		data: {
			username: userId,
			password,
		},
	});

export const apiCheckRefreshToken = (refresh: string) =>
	axios({
		method: 'post',
		url: `${BASE_URL}/token/refresh/`,
		data: {
			refresh,
		},
	});

export const apiDecodeToken = () =>
	axios({
		method: 'get',
		url: `${BASE_URL}/accounts/`,
		headers: {
			...setToken(),
		},
	});

export const apiGetUserStatus = (userId: string) =>
	axios({
		method: 'get',
		url: `${BASE_URL}/accounts/${userId}/`,
		headers: {
			...setToken(),
		},
	});

export const apiGetAdminInfo = (adminId: string) =>
	axios({
		method: 'get',
		url: `${BASE_URL}/accounts/school-admin/${adminId}/`,
		headers: {
			...setToken(),
		},
	});

export const apiGetStudentInfo = (studentId: string) =>
	axios({
		method: 'get',
		url: `${BASE_URL}/accounts/student/${studentId}/`,
		headers: {
			...setToken(),
		},
	});

export const apiGetTeacherInfo = (teacherId: string) =>
	axios({
		method: 'get',
		url: `${BASE_URL}/accounts/teacher/${teacherId}/`,
		headers: {
			...setToken(),
		},
	});

export const apiPutAdminInfo = (adminId: string, user: object) =>
	axios({
		method: 'put',
		url: `${BASE_URL}/accounts/school-admin/${adminId}/`,
		headers: {
			...setToken(),
		},
		data: {
			user,
		},
	});

export const apiPutStudentInfo = (
	studentId: string,
	user: object,
	guardianPhone: string
) =>
	axios({
		method: 'put',
		url: `${BASE_URL}/accounts/student/${studentId}/`,
		headers: {
			...setToken(),
		},
		data: {
			user,
			guardianPhone,
		},
	});

export const apiPutTeacherInfo = (teacherId: string, user: object) =>
	axios({
		method: 'put',
		url: `${BASE_URL}/accounts/teacher/${teacherId}/`,
		headers: {
			...setToken(),
		},
		data: {
			user,
		},
	});

export const apiGetStudentLectureList = (studentId: string) =>
	axios({
		method: 'get',
		url: `${BASE_URL}/accounts/student/${studentId}/lecture/`,
		headers: {
			...setToken(),
		},
	});

export const apiGetTeacherLectureList = (teacherId: string) =>
	axios({
		method: 'get',
		url: `${BASE_URL}/accounts/teacher/${teacherId}/lecture/`,
		headers: {
			...setToken(),
		},
	});

export const apiChangePassword = (
	oldPassword: string,
	newPassword: string,
	newPasswordConfirmation: string
) =>
	axios({
		method: 'put',
		url: `${BASE_URL}/accounts/password/change/`,
		headers: {
			...setToken(),
		},
		data: {
			oldPassword,
			newPassword,
			newPasswordConfirmation,
		},
	});

export const apiResetPassword = (userId: string, email: string) =>
	axios({
		method: 'put',
		url: `${BASE_URL}/accounts/password/reset/`,
		data: {
			username: userId,
			email,
		},
	});

export const apiFindId = (name: string, email: string) =>
	axios({
		method: 'post',
		url: `${BASE_URL}/accounts/username/find/`,
		data: {
			firstName: name,
			email,
		},
	});

export const apiPostProfileImg = (formData: FormData) =>
	axios({
		method: 'post',
		url: `${BASE_URL}/accounts/profile-image/`,
		headers: {
			...setToken(),
		},
		data: {
			...formData,
		},
	});
