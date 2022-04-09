import styled from 'styled-components';

const StyledItem = styled.div`
	font-size: 2em;
	text-align: center;
	color: ${props => props.theme.fontColor};
`;

function ScheduleDate() {
	return (
		<div>
			<StyledItem>오늘의 시간표</StyledItem>
		</div>
	);
}

export default ScheduleDate;
