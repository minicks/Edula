import { useContext } from 'react';
import styled from 'styled-components';
import { Link } from 'react-router-dom';
import { BsFillHouseDoorFill, BsTable, BsPeopleFill } from 'react-icons/bs';
import { FaChalkboardTeacher, FaUsers, FaUserTie } from 'react-icons/fa';
import { SiGoogleclassroom } from 'react-icons/si';
import routes from '../../routes';
import UserContext from '../../context/user';

const StyledLink = styled(Link)`
	text-decoration: none;
	font-size: 1.5em;
	color: ${props => props.theme.fontColor};
`;

const StyledList = styled.li`
	margin: 1em;
`;

const StyledContainer = styled.div`
	padding: 1em;
	width: 150px;
	min-height: 500px;
	height: 100%;
	background-color: ${props => props.theme.subBgColor};
`;

function SideBar() {
	const { userStat } = useContext(UserContext);

	const contents = (stat: string) => {
		switch (stat) {
			case 'ST':
				return (
					<>
						<StyledList>
							<StyledLink to={routes.main}>
								<BsFillHouseDoorFill /> 메인
							</StyledLink>
						</StyledList>
						<StyledList>
							<StyledLink to={routes.schedule}>
								<BsTable /> 시간표
							</StyledLink>
						</StyledList>
						<StyledList>
							<StyledLink to={routes.friend}>
								<BsPeopleFill /> 친구
							</StyledLink>
						</StyledList>
					</>
				);
			case 'TE':
				return (
					<>
						<StyledList>
							<StyledLink to={routes.main}>
								<BsFillHouseDoorFill /> 메인
							</StyledLink>
						</StyledList>
						<StyledList>
							<StyledLink to={routes.schedule}>
								<BsTable /> 시간표
							</StyledLink>
						</StyledList>
					</>
				);
			case 'SA':
				return (
					<>
						<StyledList>
							<StyledLink to={routes.admin}>
								<BsFillHouseDoorFill /> 메인
							</StyledLink>
						</StyledList>
						<StyledList>
							<StyledLink to={routes.studentManager}>
								<FaUsers /> 학생 관리
							</StyledLink>
						</StyledList>
						<StyledList>
							<StyledLink to={routes.teacherManager}>
								<FaUserTie /> 교사 관리
							</StyledLink>
						</StyledList>
						<StyledList>
							<StyledLink to={routes.classManager}>
								<SiGoogleclassroom /> 학급 관리
							</StyledLink>
						</StyledList>
						<StyledList>
							<StyledLink to={routes.lectureManager}>
								<FaChalkboardTeacher /> 수업 관리
							</StyledLink>
						</StyledList>
					</>
				);
			default:
				return null;
		}
	};

	return (
		<StyledContainer>
			<ul>{contents(userStat || '')}</ul>
		</StyledContainer>
	);
}

export default SideBar;
