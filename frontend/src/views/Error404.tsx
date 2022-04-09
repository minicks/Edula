import styled from 'styled-components';
import PageTitle from '../components/PageTitle';

const Container = styled.div`
	display: flex;
	flex-direction: column;
	text-align: center;
	padding-top: 20vh;
	font-size: 2em;
`;

function Error404() {
	return (
		<Container>
			<PageTitle title='페이지를 찾을 수 없습니다' />
			<span>Error 404: Page Not Found</span>
		</Container>
	);
}

export default Error404;
