import { Link } from 'react-router-dom';
import styled from 'styled-components';
import StyledContainer from '../schedule/StyledContainer';
import StyledTitle from './StyledTitle';

interface Props {
	students: {
		user: {
			firstName: string;
			id: number;
			status: string;
			username: string;
		};
	}[];
}

const StyledLink = styled(Link)`
	text-decoration: none;
	font-size: 1rem;
	color: ${props => props.theme.fontColor};
`;

const StyledP = styled.p`
	text-align: center;
	font-size: 1rem;
	margin: 0.3rem 0;
	border-bottom: 0.1rem solid ${props => props.theme.bgColor};
`;

function StudentList({ students }: Props) {
	return (
		<StyledContainer>
			<StyledTitle>학생 목록</StyledTitle>
			{students &&
				students.map(
					student =>
						student.user?.status === 'ST' && (
							<StyledLink to={`/profile/${student.user?.id}`} key={student.user?.id}>
								<StyledP>
									{student?.user?.username} | {student?.user?.firstName || '이름 없음'}{' '}
								</StyledP>
							</StyledLink>
						)
				)}
		</StyledContainer>
	);
}

export default StudentList;
