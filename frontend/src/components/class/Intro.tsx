import styled from 'styled-components';

const StyledTitle = styled.h1`
	font-size: 2em;
	text-align: center;
	padding: 1em;
	color: ${props => props.theme.fontColor};
`;

const StyledIntro = styled.div`
	margin: 0px;
	padding: 0px;
	background-color: ${props => props.theme.pointColor};
	background-position: center;
	background-repeat: no-repeat;
	background-size: cover;
	width: 100vw;
	min-width: 900px;
	height: 10em;
`;
interface IntroProps {
	id: number;
	name: string;
}

function Intro({ id, name }: IntroProps) {
	return (
		<StyledIntro>
			<StyledTitle>{name}</StyledTitle>
		</StyledIntro>
	);
}

export default Intro;
