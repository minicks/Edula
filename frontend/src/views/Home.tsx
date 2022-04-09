import { useContext } from 'react';
import { Navigate, Outlet } from 'react-router-dom';
import styled from 'styled-components';
import TopNavBar from '../components/navbar/TopNavBar';
import UserContext from '../context/user';
import routes from '../routes';
import SideBar from '../components/sidebar/SideBar';
import Footer from '../components/footer/Footer';

const OutletContainer = styled.div`
	display: flex;
	flex-direction: column;
	align-items: center;
	min-height: 500px;
	height: 100%;
`;

const BodyWrapper = styled.div`
	display: flex;
	min-height: 100vh;
	flex-direction: column;
`;
const BodyContent = styled.div`
	flex: 1;
`;
const Container = styled.div`
	display: grid;
	grid-template-columns: 1fr 6fr;
`;

function Main() {
	const { isLoggedIn } = useContext(UserContext);

	if (!isLoggedIn) {
		return <Navigate to={routes.login} />;
	}

	return (
		<BodyWrapper>
			<BodyContent>
				<TopNavBar />
				<Container>
					<SideBar />

					<OutletContainer>
						<Outlet />
					</OutletContainer>
				</Container>
			</BodyContent>
			<Footer />
		</BodyWrapper>
	);
}

export default Main;
