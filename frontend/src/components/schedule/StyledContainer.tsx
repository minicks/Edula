import styled from 'styled-components';

const StyledContainer = styled.div`
	width: 25em;
	margin: 1em;
	padding: 1em;
	color: ${props => props.theme.fontColor};
	background-color: ${props => props.theme.subBgColor};
	border-radius: 4px;
	box-shadow: 0 1px 3px black;
`;

export default StyledContainer;
