import styled from 'styled-components';

const StyledContent = styled.div`
	margin: 1em;
	font-size: 1em;
	text-align: center;
	background: ${props => props.theme.subBgColor};
	color: ${props => props.theme.fontColor};
	padding: 2em 2em 2em 2em;
	box-shadow: 0 1px 1px rgba(0, 0, 0, 0.125);
	border-radius: 10px;
`;
export default StyledContent;
