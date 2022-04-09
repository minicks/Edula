import styled from 'styled-components';

const StyledItem = styled.div`
	background-color: ${props => props.theme.pointColor};
	margin: 0.5rem;
	padding: 0.3rem;
	text-align: center;
	color: ${props => props.theme.fontColor};
	border-radius: 4px;
	box-shadow: 0 1px 1px black;
`;

export default StyledItem;
