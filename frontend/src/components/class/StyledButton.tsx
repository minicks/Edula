import styled from 'styled-components';

const StyledButton = styled.button`
	display: inline-block;
	font-size: 1em;
	padding: 1em 2em;
	margin: 1em 0.5em;
	-webkit-appearance: none;
	appearance: none;
	background-color: $button-bg;
	color: $button-text-color;
	border-radius: 4px;
	border: none;
	cursor: pointer;
	position: relative;
`;

export default StyledButton;
