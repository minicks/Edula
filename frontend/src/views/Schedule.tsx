import styled from 'styled-components';
import PageTitle from '../components/PageTitle';
import ScheduleAllContainer from '../components/schedule/ScheduleAllContainer';
import ScheduleContainer from '../components/schedule/ScheduleContainer';

const Container = styled.div`
	display: flex;
	flex-direction: column;
	justify-content: center;
	align-items: center;
	width: 100%;
	margin: 20px;
`;

function Schedule() {
	return (
		<Container>
			<PageTitle title='오늘의 일정' />
			<ScheduleContainer />
			<ScheduleAllContainer />
		</Container>
	);
}

export default Schedule;
