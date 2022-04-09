import styled from 'styled-components';
import Logo from './LogoBtn';
import Alert from './AlarmBtn';
import Profile from './ProfileBtn';

const StyledNav = styled.nav`
	display: flex;
	align-items: center;
	justify-content: space-between;
	padding: 0.375rem 0.75rem;
	line-height: 1.5;
	border-bottom: 1px solid ${props => props.theme.borderColor};
	color: ${props => props.theme.subBgColor};
	font-size: 3rem;
	width: 100%;
	box-sizing: border-box;
	background-color: ${props => props.theme.mainBlue};
`;

const StyledSpan = styled.span`
	display: flex;
	align-items: center;
`;

function TopNavBar() {
	return (
		<StyledNav>
			<Logo />
			<StyledSpan>
				<Alert />
				<Profile />
			</StyledSpan>
		</StyledNav>
	);
}

export default TopNavBar;
