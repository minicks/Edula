import { ReactNode } from 'react';
import styled from 'styled-components';

const STable = styled.div`
	width: 100%;
	box-sizing: border-box;
	margin-top: 20px;
`;

type PropType = {
	children: ReactNode;
};

function Table({ children }: PropType) {
	return <STable>{children}</STable>;
}

export default Table;
