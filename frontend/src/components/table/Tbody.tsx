import { ReactNode } from 'react';
import styled from 'styled-components';

const STbody = styled.div`
	display: flex;
`;

type PropType = {
	children: ReactNode;
};

function Tbody({ children }: PropType) {
	return <STbody>{children}</STbody>;
}

export default Tbody;
