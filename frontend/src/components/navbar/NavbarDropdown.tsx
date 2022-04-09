import { useContext, useRef } from 'react';
import { Link } from 'react-router-dom';
import styled, { css } from 'styled-components';
import UserContext from '../../context/user';
import routes from '../../routes';
import { useDetectOutsideClick } from '../useDetectOutsideClick';
import StyledDeleteBtn from '../friend/StyledDeleteBtn';
import { BASE_URL } from '../../api/utils';

const StyledContainer = styled.div`
	box-sizing: border-box;
`;
const StyledMenuContainer = styled.div`
	position: relative;
	display: flex;
	justify-content: center;
	align-items: center;
`;

const StyledMenuTrigger = styled.button`
	background: ${props => props.theme.subBgColor};
	border-radius: 50%;
	cursor: pointer;
	display: flex;
	justify-content: space-between;
	align-items: center;
	padding: 3px;
	box-shadow: 0 1px 3px ${props => props.theme.fontColor};
	border: none;
	vertical-align: middle;
	transition: box-shadow 0.4s ease;
	margin-left: auto;

	:hover {
		box-shadow: 0 1px 8px ${props => props.theme.fontColor};
	}

	img {
		border-radius: 50%;
		width: 50px;
		height: 50px;
	}
`;

interface MenuProp {
	isactive: string;
}
const StyledLogoutBtn = styled(StyledDeleteBtn)`
	font-size: 0.5rem;
	background: ${props => props.theme.pointColor};
	color: ${props => props.theme.fontColor};
	box-shadow: 0 1px 3px black;
`;

const StyledMenu = styled.nav<MenuProp>`
	background: ${props => props.theme.subBgColor};
	border-radius: 8px;
	position: absolute;
	top: 3.5rem;
	right: 0;
	width: 10rem;
	box-shadow: 0 1px 8px ${props => props.theme.fontColor};
	opacity: 0;
	visibility: hidden;
	transform: translateY(-20px);
	transition: opacity 0.4s ease, transform 0.4s ease, visibility 0.4s;
	${props =>
		props.isactive === 'active' &&
		css`
			opacity: 1;
			visibility: visible;
			transform: translateY(0);
		`}

	ul {
		list-style: none;
		padding: 0;
		margin: 0;
	}

	li {
		display: flex;
		justify-content: center;
		border-bottom: 1px solid ${props => props.theme.subBgColor};
		border-radius: 50%;
	}

	li a {
		text-align: center;
		font-size: 1rem;
		text-decoration: none;
		color: ${props => props.theme.fontColor};
		padding: 0.4rem 1rem;
		display: block;
	}

	button {
		text-align: center;
		border: none;
		background-color: inherit;
		cursor: pointer;
		padding: 0.4rem 1rem;
	}
`;

function NavbarDropdown() {
	const dropdownRef = useRef(null);
	const [isActive, setIsActive] = useDetectOutsideClick(dropdownRef, false);
	const onClick = () => setIsActive(!isActive);
	const { logout, userId } = useContext(UserContext);
	const { profileImg } = useContext(UserContext);

	return (
		<StyledContainer>
			<StyledMenuContainer>
				<StyledMenuTrigger type='button' onClick={onClick}>
					<img
						src={
							profileImg
								? `${process.env.REACT_APP_PROTOCOL}://${window.location.hostname}:${process.env.REACT_APP_PORT}${profileImg}`
								: 'https://phinf.pstatic.net/contact/20201125_191/1606304847351yz0f4_JPEG/KakaoTalk_20201007_183735541.jpg?type=f130_130'
						}
						alt='User avatar'
					/>
				</StyledMenuTrigger>
				<StyledMenu ref={dropdownRef} isactive={isActive ? 'active' : 'inactive'}>
					<ul>
						<li>
							<Link to={`${routes.profile}/${userId}`} onClick={onClick}>
								My Profile
							</Link>
						</li>
						<li>
							<Link to={routes.setting} onClick={onClick}>
								Settings
							</Link>
						</li>
						<li>
							<StyledLogoutBtn type='button' onClick={logout}>
								로그 아웃
							</StyledLogoutBtn>
						</li>
					</ul>
				</StyledMenu>
			</StyledMenuContainer>
		</StyledContainer>
	);
}

export default NavbarDropdown;
