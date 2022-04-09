import { useContext, useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import styled from 'styled-components';
import { apiGetClassrooms } from '../../api/classroom';
import { apiGetLectures } from '../../api/lecture';
import { apiGetStudents, apiGetTeachers } from '../../api/school';
import PageTitle from '../../components/PageTitle';
import UserContext from '../../context/user';
import routes from '../../routes';

const Container = styled.div`
	display: flex;
	flex-direction: column;
	align-items: center;
	justify-content: center;
	padding: 2em;
`;

const SLink = styled(Link)`
	text-decoration: none;
`;

const Title = styled.div`
	font-size: 2.5em;
`;

const Contents = styled.div`
	display: flex;
	flex-wrap: wrap;
`;

const Section = styled.div`
	min-width: 20em;
	height: 10em;
	display: flex;
	flex-direction: column;
	align-items: center;
	background-color: ${props => props.theme.subBgColor};
	border-radius: 1px;
	margin: 1em;
`;

const SectionTitle = styled.div`
	font-size: 1.5em;
	margin: 0.5em;
`;

const SectionContents = styled.div`
	display: flex;
	flex-direction: column;
	align-items: center;
`;

interface Classroom {
	id: number;
	classGrade: number;
	classNum: number;
	school: number;
}

interface School {
	id: number;
	name: string;
	abbreviation: string;
}

interface User {
	id: number;
	username?: string;
	firstName?: string;
	status?: string;
	email?: string;
	phone?: string;
}

interface Student {
	classroom?: Classroom;
	guardianPhone?: string;
	school?: School;
	user: User;
}

interface Teacher {
	classroom?: Classroom;
	school?: School;
	user: User;
}

interface Lecture {
	id: number;
	name: string;
	school: number;
	studentList: Array<number>;
	teacher: User;
	timeList: TimeList;
}

type TimeList = {
	count: number;
	lectures: Array<LectureList>;
};

type LectureList = {
	day: string;
	st: string;
	end: string;
};

function AdminIndex() {
	const { schoolId } = useContext(UserContext);
	const [students, setStudents] = useState([] as Student[]);
	const [teachers, setTeachers] = useState([] as Teacher[]);
	const [classrooms, setClassrooms] = useState([] as Classroom[]);
	const [lectures, setLectures] = useState([] as Array<Lecture>);

	const getStudents = () => {
		apiGetStudents(schoolId).then(res => {
			setStudents(res.data);
		});
	};

	const getTeachers = () => {
		apiGetTeachers(schoolId).then(res => {
			setTeachers(res.data);
		});
	};

	const getClassrooms = () => {
		apiGetClassrooms(schoolId).then(res => {
			setClassrooms(res.data);
		});
	};

	const getLectures = () => {
		apiGetLectures().then(res => {
			setLectures(res.data);
		});
	};

	useEffect(() => {
		if (schoolId) {
			getStudents();
			getTeachers();
			getClassrooms();
			getLectures();
		}
	}, [schoolId]);

	return (
		<Container>
			<PageTitle title='관리자 페이지' />
			<Title>관리자 페이지입니다.</Title>
			<Contents>
				<SLink to={routes.studentManager}>
					<Section>
						<SectionTitle>학생 현황</SectionTitle>
						<SectionContents>총 학생 수 : {students.length} 명</SectionContents>
					</Section>
				</SLink>
				<SLink to={routes.teacherManager}>
					<Section>
						<SectionTitle>교사 현황</SectionTitle>
						<SectionContents>총 교사 수 : {teachers.length}</SectionContents>
					</Section>
				</SLink>
				<SLink to={routes.classManager}>
					<Section>
						<SectionTitle>학급 현황</SectionTitle>
						<SectionContents>총 학급 수 : {classrooms.length}</SectionContents>
					</Section>
				</SLink>
				<SLink to={routes.lectureManager}>
					<Section>
						<SectionTitle>수업 현황</SectionTitle>
						<SectionContents>총 수업 수 : {lectures.length}</SectionContents>
					</Section>
				</SLink>
			</Contents>
		</Container>
	);
}

export default AdminIndex;
