import { ReactNode } from 'react';
import styled from 'styled-components';

const Container = styled.div`
	display: flex;
	justify-content: center;
	align-items: center;
	height: 100vh;
`;

const Wrapper = styled.div`
	max-width: 420px;
	width: 100%;
	padding: 20px;
	background-color: ${props => props.theme.subBgColor};
	border-radius: 3px;
	display: flex;
	flex-direction: column;
	justify-content: center;
	align-items: center;
`;

type PropType = {
	children: ReactNode;
};

function AuthLayout({ children }: PropType) {
	return (
		<Container>
			<Wrapper>{children}</Wrapper>
		</Container>
	);
}

export default AuthLayout;
