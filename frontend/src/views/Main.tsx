import { useContext, useEffect, useState } from 'react';
import styled from 'styled-components';
import { useNavigate } from 'react-router-dom';
import {
	apiGetStudentLectureList,
	apiGetTeacherLectureList,
} from '../api/user';
import StyledTitle from '../components/class/StyledTitle';
import ScheduleContainer from '../components/schedule/ScheduleContainer';
import UserContext from '../context/user';
import routes from '../routes';
import Btn from '../common/Btn';
import PageTitle from '../components/PageTitle';

const StyledContainer = styled.div`
	display: flex;
	flex-direction: column;
	justify-content: center;
	align-items: center;
	/* width: 100%; */
	margin: 20px;
`;

function Home() {
	const navigate = useNavigate();
	const { currentLecture, changeCurrentLecture, userStat, userId, userName } =
		useContext(UserContext);
	const [currentDate, setCurrentDate] = useState(new Date());
	const [lectures, setLectures] = useState();

	const getLectures = async () => {
		switch (userStat) {
			case 'ST':
				await apiGetStudentLectureList(userId).then(res => console.log(res));
				break;
			case 'TE':
				await apiGetTeacherLectureList(userId).then(res => console.log(res));
				break;
			default:
				break;
		}
	};

	useEffect(() => {
		getLectures();
	}, []);

	console.log(
		currentDate.getHours(),
		currentDate.getMinutes(),
		currentDate.getDay()
	);

	return (
		<StyledContainer>
			<PageTitle title={`${userName || '회원'}님 환영합니다`} />
			<StyledTitle>오늘도 화이팅! </StyledTitle>
			<ScheduleContainer />
			<Btn onClick={() => navigate(routes.conference)}>
				{currentLecture} 수업 입장
			</Btn>
		</StyledContainer>
	);
}

export default Home;
