import { createContext } from 'react';

const UserContext = createContext({
	isLoggedIn: false,
	login: (_: string, __: string) => {},
	logout: () => {},
	userId: '',
	userName: '',
	userStat: '',
	schoolId: '',
	currentLecture: '',
	changeCurrentLecture: (_: string) => {},
	profileImg: '',
	changeProfileImg: (_: string) => {},
});

export default UserContext;
