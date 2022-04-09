import { ReactNode } from 'react';
import styled from 'styled-components';

const SBtn = styled.button`
	background-color: ${props => props.theme.pointColor};
	color: ${props => props.theme.fontColor};
	width: 100%;
	padding: 3px;
	border-radius: 3px;
	font-size: 1rem;
`;

type PropType = {
	children: ReactNode;
	onClick: () => void;
};

function Btn({ children, onClick }: PropType) {
	return (
		<SBtn type='button' onClick={onClick}>
			{children}
		</SBtn>
	);
}

export default Btn;
