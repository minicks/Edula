import styled from 'styled-components';
import FriendList from '../components/friend/FriendList';
import FriendGivenRequest from '../components/friend/FriendRequest';
import FriendSearch from '../components/friend/FriendSearch';
import MessageList from '../components/message/MessageList';
import PageTitle from '../components/PageTitle';

const Container = styled.div`
	display: flex;
	flex-wrap: wrap;
`;
function Friend() {
	return (
		<Container>
			<PageTitle title='친구~~' />
			<FriendList />
			<FriendSearch />
			<FriendGivenRequest />
			<MessageList />
		</Container>
	);
}

export default Friend;
