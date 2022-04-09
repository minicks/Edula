import styled from 'styled-components';

const LinkBox = styled.div`
	width: 100%;
	padding-top: 10px;
	display: flex;
	align-items: center;

	a {
		text-decoration: none;
		margin: 0px 3px;
		font-size: 0.8rem;
		color: ${props => props.theme.fontColor};
		&:hover {
			text-decoration: underline;
		}
	}
`;

export default LinkBox;
