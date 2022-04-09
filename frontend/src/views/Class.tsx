import { useEffect, useState, useContext } from 'react';
import { useParams } from 'react-router-dom';
import styled from 'styled-components';
import Intro from '../components/class/Intro';
import { apiGetLectureDetail } from '../api/lecture';
import { apiGetHomeworks } from '../api/homework';
import ArticleBoard from '../components/class/ArticleBoard';
import HomeworkBoard from '../components/class/HomeworkBoard';
import StudentList from '../components/class/StudentList';
import UserContext from '../context/user';
import PageTitle from '../components/PageTitle';

const StyledContainer = styled.section`
	display: flex;
	flex-direction: row;
	align-items: flex-start;
	justify-content: space-evenly;
`;

interface LectureDataType {
	id: number;
	name: string;
	timeList: {
		count: number;
		lectures: [
			{
				day: string;
				st: string;
				end: string;
			}
		];
	};
	school: number;
	teacher: number;
	studentList: {
		user: {
			firstName: string;
			id: number;
			status: string;
			username: string;
		};
	}[];
}

const StyledIntro = styled(Intro)``;

function Class() {
	const [lectureData, setLectureData] = useState({} as LectureDataType);
	const [homeworkData, setHomeworkData] = useState(null);
	const { userStat } = useContext(UserContext);
	const { lectureId } = useParams();

	useEffect(() => {
		if (lectureId) {
			apiGetLectureDetail(lectureId).then(res => {
				setLectureData(res.data);
			});
		}
	}, []);

	useEffect(() => {
		if (lectureId) {
			apiGetHomeworks(lectureId).then(res => {
				setHomeworkData(res.data.homework);
			});
		}
	}, []);

	if (lectureData) {
		return (
			<>
				<PageTitle title={`${lectureData.name} 페이지`} />
				<StyledIntro id={lectureData.id} name={lectureData.name} />
				<StyledContainer>
					{homeworkData && <HomeworkBoard homeworks={homeworkData} />}
					<ArticleBoard />
					{userStat === 'TE' && <StudentList students={lectureData.studentList} />}
				</StyledContainer>
			</>
		);
	}
	return <h1>로딩 중</h1>;
}

export default Class;
