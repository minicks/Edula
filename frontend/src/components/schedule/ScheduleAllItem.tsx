import { Link } from 'react-router-dom';
import styled from 'styled-components';
import StyledItem from './StyledItem';

interface ScheduleItemProps {
	scheduleId: number;
	name: string;
}

const StyledLink = styled(Link)`
	text-decoration: none;
`;

function ScheduleAllItem({ scheduleId, name }: ScheduleItemProps) {
	if (name) {
		return (
			<StyledLink to={`/lecture/${scheduleId}/`}>
				<StyledItem>{name}</StyledItem>
			</StyledLink>
		);
	}
	return <h1>수업 없다 !</h1>;
}

export default ScheduleAllItem;
