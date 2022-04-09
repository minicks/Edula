import { useEffect, useState, useContext } from 'react';
import StyledContainer from './StyledContainer';
import ScheduleAllItem from './ScheduleAllItem';
import {
	apiGetStudentLectureList,
	apiGetUserStatus,
	apiGetTeacherLectureList,
} from '../../api/user';
import UserContext from '../../context/user';
import StyledTitle from '../class/StyledTitle';

interface ScheduleDataType {
	id: number;
	name: string;
	timeList: {
		count: number;
		lectures: {
			day: string;
			st: string;
			end: string;
		}[];
	};
	school: number;
	teacher: number;
	studentList: number[];
}

function ScheduleAllContainer() {
	const { userId } = useContext(UserContext);
	const [userStat, setUserStat] = useState('');
	const [scheduleData, setScheduleData] = useState(
		[] as Array<ScheduleDataType>
	);

	useEffect(() => {
		if (userId) {
			apiGetUserStatus(userId || '')
				.then(res => {
					setUserStat(res.data.status);
				})
				.catch(() => {});
		}
	}, [userId]);

	useEffect(() => {
		if (userStat) {
			switch (userStat) {
				case 'ST':
					apiGetStudentLectureList(userId || '').then(res => {
						setScheduleData(res.data?.lectureList);
					});
					break;

				case 'TE':
					apiGetTeacherLectureList(userId || '').then(res => {
						setScheduleData(res.data?.lectureList);
					});
					break;

				default:
					break;
			}
		}
	}, [userStat]);

	if (scheduleData) {
		return (
			<StyledContainer>
				<StyledTitle>모든 수업</StyledTitle>
				{scheduleData.map(sub => (
					<ScheduleAllItem key={sub.id} scheduleId={sub.id} name={sub.name} />
				))}

				{scheduleData.length === 0 && <StyledTitle>수업이 없어요!</StyledTitle>}
			</StyledContainer>
		);
	}
	return <h1>로딩 중</h1>;
}

export default ScheduleAllContainer;
