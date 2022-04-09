import styled from 'styled-components';

const StyledButton = styled.button`
	display: inline;
	font-size: 1em;
	padding: 0.5em;
	margin: 1em 0.5em;
	-webkit-appearance: none;
	appearance: none;
	background: ${props => props.theme.warningColor};
	color: white;
	border-radius: 4px;
	border: none;
	cursor: pointer;
	position: relative;
`;

export default StyledButton;
