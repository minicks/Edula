import { ReactNode } from 'react';
import styled from 'styled-components';

const SBtn = styled.button`
	border: none;
	background-color: inherit;
	color: ${props => props.theme.fontColor};
	cursor: pointer;
`;

type PropType = {
	children: ReactNode;
	onClick: () => void;
};

function IconBtn({ children, onClick }: PropType) {
	return (
		<SBtn type='button' onClick={onClick}>
			{children}
		</SBtn>
	);
}

export default IconBtn;
