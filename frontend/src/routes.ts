const routes = {
	// auth
	login: '/login',
	findid: '/findid',
	findpw: '/findpw',
	signup: '/signup',

	main: '/',

	conference: '/conference',
	setting: '/setting',
	profile: '/profile',
	alarm: '/alarm',
	class: '/lecture/:lectureId',
	classroom: '/classroom',
	createarticle: '/:lectureId/articleCreate',
	updatearticle: '/:lectureId/articleUpdate/:articleId',
	articleDetail: '/:lectureId/article/:articleId',

	createHomework: '/:lectureId/homeworkCreate',
	updateHomework: '/:lectureId/homeworkUpdate/:homeworkId',
	homeworkDetail: '/:lectureId/homework/:homeworkId',
	homeworkSubmit: '/:lectureId/homework/:homeworkId/submit',
	homeworkSubmitDetail: '/:lectureId/homework/:homeworkId/submit/:userId',

	schedule: '/schedule',
	friend: '/friend',
	// Admin Page
	admin: '/manage',
	studentManager: '/manage/student',
	teacherManager: '/manage/teacher',
	classManager: '/manage/class',
	lectureManager: '/manage/lecture',
};

export default routes;
