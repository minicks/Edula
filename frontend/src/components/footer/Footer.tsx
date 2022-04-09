import styled from 'styled-components';
import { BsGithub, BsYoutube } from 'react-icons/bs';

const StyledFooter = styled.footer`
	margin: 0px auto;
	width: 100%;
	background-color: ${props => props.theme.mainBlue};
	padding: 0 0 1rem 0;
	color: ${props => props.theme.fontColor};
`;

const StyledContainer = styled.div`
	display: flex;
	flex-wrap: wrap;
	justify-content: space-around;
`;

const StyledUl = styled.ul`
	list-style: none;
	padding-left: 0;
`;

const StyledTitle = styled.h3`
	font-size: 1.375rem;
	padding-bottom: 0.625rem;
`;

const StyledA = styled.a`
	color: ${props => props.theme.fontColor};
	text-decoration: none;
	margin: 0.3rem;
`;
const StyledDiv = styled.div`
	text-align: center;
	padding: 0.5rem;
`;

const StyledNav = styled.nav`
	text-align: center;
`;
const StyledLi = styled.li`
	margin: 0.3rem;
`;

const StyledShapedFill = styled.path`
	fill: ${props => props.theme.bgColor};
`;

const StyledSVG = styled.svg`
	position: relative;
	display: block;
	width: calc(100% + 1.3px);
	height: 150px;
`;
function Footer() {
	return (
		<StyledFooter>
			<StyledSVG
				data-name='Layer 1'
				xmlns='http://www.w3.org/2000/svg'
				viewBox='0 0 1200 120'
				preserveAspectRatio='none'
			>
				<StyledShapedFill d='M321.39,56.44c58-10.79,114.16-30.13,172-41.86,82.39-16.72,168.19-17.73,250.45-.39C823.78,31,906.67,72,985.66,92.83c70.05,18.48,146.53,26.09,214.34,3V0H0V27.35A600.21,600.21,0,0,0,321.39,56.44Z' />
			</StyledSVG>
			<StyledContainer>
				<StyledUl>
					<StyledTitle>정보</StyledTitle>
					<StyledLi>
						<StyledA href='https://www.youtube.com/'>학교 관리자용 설명</StyledA>
					</StyledLi>

					<StyledLi>
						<StyledA href='https://www.youtube.com/'>교사용 설명</StyledA>
					</StyledLi>
					<StyledLi>
						<StyledA href='https://www.youtube.com/'>학생용 설명</StyledA>
					</StyledLi>
				</StyledUl>
				<StyledUl>
					<StyledTitle>문의</StyledTitle>
					<address>이메일: edula.gugugugugugu@gmail.com</address>
				</StyledUl>
			</StyledContainer>

			<StyledDiv>
				<p>Edula/에두라</p>
			</StyledDiv>
			<StyledNav>
				<StyledA href='https://github.com/'>
					<BsGithub />
				</StyledA>

				<StyledA href='https://www.youtube.com/'>
					<BsYoutube />
				</StyledA>
			</StyledNav>
			<StyledDiv>
				Copyrightⓒ2022 SSAFY 6th team Bibapgu All rights reserved.
			</StyledDiv>
		</StyledFooter>
	);
}

export default Footer;
