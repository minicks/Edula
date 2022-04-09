import { useEffect, useState, useContext } from 'react';
import styled from 'styled-components';
import StyledTitle from '../class/StyledTitle';
import StyledContainer from '../friend/StyledContainer';
import {
	apiDeleteMessage,
	apiPatchMessage,
	apiGetMessageCnt,
	apiGetMessages,
} from '../../api/directMessage';
import StyledDeleteBtn from '../friend/StyledDeleteBtn';
import Pagination from '../class/ArticlePagination';
import UserContext from '../../context/user';

const StyledReadBtn = styled(StyledDeleteBtn)`
	background: ${props => props.theme.bgColor};
	color: ${props => props.theme.fontColor};
	box-shadow: 0 1px 3px black;
`;
const ReadMessage = styled.p`
	opacity: 0.5;
`;

const StyledMessageDeleteBtn = styled(StyledDeleteBtn)`
	background: ${props => props.theme.borderColor};
	color: ${props => props.theme.fontColor};
	box-shadow: 0 1px 3px black;
`;
interface MessageType {
	id: number;
	fromUser: {
		id: number;
		username: string;
		firstName: string;
		status: string;
		profileImage: string;
	};
	content: string;
	time: string;
	send: boolean;
	read: boolean;
}

function MessageList() {
	const { userId } = useContext(UserContext);
	const [totalMessageCnt, setTotalMessageCnt] = useState(0);
	const [messageCnt, setMessageCnt] = useState(0);

	const [limit] = useState(5);
	const [page, setPage] = useState(1);
	const [sendPage, setSendPage] = useState(1);
	const [total, setTotal] = useState(0);
	const [sendTotal, setSendTotal] = useState(0);

	const [messages, setMessages] = useState([] as Array<MessageType>);
	const [sendMessages, setSendMessages] = useState([] as Array<MessageType>);

	const getTotalMessageCnt = () => {
		apiGetMessageCnt()
			.then(res => {
				setTotalMessageCnt(res.data.countAll);
				setMessageCnt(res.data.count);
			})
			.catch();
	};

	const getMessages = () => {
		apiGetMessages('0', page.toString(), limit.toString())
			.then(res => {
				// console.log(res.data);
				setMessages(res.data.messages);
				setTotal(res.data.totalCount);
			})
			.catch(() => {});
	};

	const getSendMessages = () => {
		apiGetMessages(userId.toString(), page.toString(), limit.toString())
			.then(res => {
				setSendMessages(res.data.messages);
				setSendTotal(res.data.totalCount);
			})
			.catch(() => {});
	};

	useEffect(() => {
		getMessages();
	}, [page, limit, totalMessageCnt]);

	useEffect(() => {
		getSendMessages();
	}, [sendPage, limit, sendTotal, userId]);

	useEffect(() => {
		getTotalMessageCnt();
	}, []);

	return (
		<>
			<StyledContainer>
				<StyledTitle>받은 쪽지</StyledTitle>
				<p>
					안 읽은 쪽지: {messageCnt} / 전체 쪽지: {totalMessageCnt}
				</p>

				{messages &&
					messages.map(message => (
						<div key={message.id}>
							{!message.send && !message.read && (
								<p key={message.id}>
									{message.time.slice(0, 10)} {message.time.slice(11, 18)}|{' '}
									{message.fromUser?.username} (
									{message.fromUser?.firstName || '이름 없음'}) : {message.content}
									<StyledReadBtn
										onClick={e => {
											e.preventDefault();

											try {
												apiPatchMessage(
													message.fromUser?.id.toString(),
													message.id.toString()
												);
												window.location.reload();
											} catch (error) {
												// console.log(error);
											}
										}}
									>
										읽음
									</StyledReadBtn>
									<StyledMessageDeleteBtn
										onClick={e => {
											e.preventDefault();

											try {
												apiDeleteMessage(
													message.fromUser?.id.toString(),
													message.id.toString()
												).then(() => {
													window.location.reload();
												});
											} catch (error) {
												// console.log(error);
											}
										}}
									>
										삭제
									</StyledMessageDeleteBtn>
								</p>
							)}
							{!message.send && message.read && (
								<ReadMessage key={message.id}>
									{message.time.slice(0, 10)} {message.time.slice(11, 18)}| |{' '}
									{message.fromUser?.username} (
									{message.fromUser?.firstName || '이름 없음'}) : {message.content}
									<StyledMessageDeleteBtn
										onClick={e => {
											e.preventDefault();

											try {
												apiDeleteMessage(
													message.fromUser?.id.toString(),
													message.id.toString()
												).then(() => {
													window.location.reload();
												});
											} catch (error) {
												// console.log(error);
											}
										}}
									>
										삭제
									</StyledMessageDeleteBtn>
								</ReadMessage>
							)}
						</div>
					))}
				{messages.length === 0 && (
					<StyledTitle>새로운 메시지가 없어요~</StyledTitle>
				)}
				{messages.length !== 0 && (
					<footer>
						<Pagination total={total} limit={limit} page={page} setPage={setPage} />
					</footer>
				)}
			</StyledContainer>

			<StyledContainer>
				<StyledTitle>보낸 쪽지</StyledTitle>
				{sendMessages &&
					sendMessages.map(message => (
						<p key={message.id}>
							{message.time.slice(0, 10)} {message.time.slice(11, 18)}|{' '}
							{message.fromUser?.username} (
							{message.fromUser?.firstName || '이름 없음'}) : {message.content}
							<StyledMessageDeleteBtn
								onClick={e => {
									e.preventDefault();

									try {
										apiDeleteMessage(
											message.fromUser?.id.toString(),
											message.id.toString()
										).then(() => {
											window.location.reload();
										});
									} catch (error) {
										// console.log(error);
									}
								}}
							>
								삭제
							</StyledMessageDeleteBtn>
						</p>
					))}
				{sendMessages.length === 0 && (
					<StyledTitle>보낸 메시지가 없어요~</StyledTitle>
				)}
				{sendMessages.length !== 0 && (
					<footer>
						<Pagination
							total={sendTotal}
							limit={limit}
							page={sendPage}
							setPage={setSendPage}
						/>
					</footer>
				)}
			</StyledContainer>
		</>
	);
}

export default MessageList;
