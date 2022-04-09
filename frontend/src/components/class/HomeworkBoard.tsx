import { useContext } from 'react';
import styled from 'styled-components';
import { Link, useParams } from 'react-router-dom';
import StyledTitle from './StyledTitle';
import StyledButton from './StyledButton';
import UserContext from '../../context/user';
import StyledContent from './StyledContent';

const StyledListItem = styled.li`
	font-size: 1em;
	text-align: center;
	margin: 1em;
	background: ${props => props.theme.subBgColor};
	color: ${props => props.theme.fontColor};
	padding: 1em 2em;
	box-shadow: 0 1px 1px rgba(0, 0, 0, 0.125);
	border-radius: 10px;
`;

const StyledLink = styled(Link)`
	text-decoration: none;
	font-size: 1em;
`;

const StyledContainer = styled.div`
	margin: 0 3em;
`;

interface BoardProps {
	homeworks: {
		content: string;
		createdAt: string;
		deadline: string;
		id: number;
		lecture: number;
		title: string;
		writer: number;
	}[];
}
function HomeworkBoard({ homeworks }: BoardProps) {
	const { userStat } = useContext(UserContext);
	const { lectureId } = useParams();

	return (
		<StyledContainer>
			<StyledTitle>과제</StyledTitle>
			<ul>
				{homeworks &&
					homeworks?.map(homework => (
						<StyledLink
							to={`/${lectureId}/homework/${homework.id}`}
							key={homework.id}
						>
							<StyledListItem>
								<StyledContent>{homework.title}</StyledContent>
								<p>{homework.deadline?.slice(0, 10)}</p>
							</StyledListItem>
						</StyledLink>
					))}
			</ul>
			{homeworks.length === 0 && <StyledTitle>과제가 없어요!</StyledTitle>}
			{userStat === 'TE' && (
				<Link to={`/${lectureId}/homeworkCreate`}>
					<StyledButton>과제 등록</StyledButton>
				</Link>
			)}
		</StyledContainer>
	);
}

export default HomeworkBoard;
