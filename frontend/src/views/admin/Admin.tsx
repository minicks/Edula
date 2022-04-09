import { Outlet } from 'react-router-dom';
import styled from 'styled-components';

const OutletContainer = styled.div`
	display: flex;
	flex-direction: column;
	align-items: center;
	padding: 0 0 0 20px;
`;

function Admin() {
	return (
		<OutletContainer>
			<Outlet />
		</OutletContainer>
	);
}

export default Admin;
