import axios from 'axios';
import { BASE_URL, setToken } from './utils';

export const apiGetStudents = (schoolId: string) =>
	axios({
		method: 'get',
		url: `${BASE_URL}/schools/${schoolId}/student/`,
		headers: {
			...setToken(),
		},
	});

export const apiGetTeachers = (schoolId: string) =>
	axios({
		method: 'get',
		url: `${BASE_URL}/schools/${schoolId}/teacher/`,
		headers: {
			...setToken(),
		},
	});
