import { useEffect, useState, useRef } from 'react';
import styled from 'styled-components';
import { Link } from 'react-router-dom';
import StyledTitle from '../class/StyledTitle';
import { apiGetFriendList, apiDeleteFriend } from '../../api/friend';
import { apiPostMessage } from '../../api/directMessage';
import StyledDiv from './StyledDiv';
import StyledContainer from './StyledContainer';
import StyledDeleteBtn from './StyledDeleteBtn';

interface FriendDataType {
	id: number;
	username: string;
	firstname: string;
	status: string;
}
const StyledSendBtn = styled(StyledDeleteBtn)`
	background: ${props => props.theme.pointColor};
	color: ${props => props.theme.fontColor};
	box-shadow: 0 1px 3px black;
`;
const StyledLink = styled(Link)`
	text-decoration: none;
	font-size: 1em;
`;
const StyledSpan = styled.span`
	color: ${props => props.theme.fontColor};
`;
const StyledMessageBtn = styled(StyledDeleteBtn)`
	background: ${props => props.theme.bgColor};
	color: ${props => props.theme.fontColor};
	box-shadow: 0 1px 3px black;
`;

const StyledInput = styled.input`
	border-top: none;
	border-left: none;
	border-right: none;
	border-bottom: 3px solid ${props => props.theme.mainBlue};
	width: 16rem;
	height: 2rem;
	border-radius: 4px;
`;

function FriendList() {
	const inputRef = useRef<HTMLInputElement>(null);
	const [isModalOn, setIsModalOn] = useState(false);
	const [pickedFriend, setPickedFriend] = useState(0);
	const [pickedFriendName, setPickedFriendName] = useState('');
	const [friendList, setFriendList] = useState([] as FriendDataType[]);
	const getFriendList = () => {
		apiGetFriendList().then(res => {
			setFriendList(res.data);
		});
	};

	useEffect(() => {
		getFriendList();
	}, []);

	return (
		<div>
			<StyledContainer>
				<StyledTitle>친구 목록</StyledTitle>
				{isModalOn && (
					<form>
						<StyledInput
							type='text'
							name='text'
							ref={inputRef}
							placeholder={`${pickedFriendName || '친구'}에게 예쁜 말을 보내줘요.`}
						/>
						<StyledSendBtn
							type='submit'
							onClick={e => {
								e.preventDefault();
								if (inputRef?.current?.value) {
									try {
										apiPostMessage(pickedFriend.toString(), inputRef?.current?.value);
										setIsModalOn(false);
									} catch (error) {
										// console.log(error);
									}
								}
							}}
						>
							쪽지 보내기
						</StyledSendBtn>
					</form>
				)}
				{friendList &&
					friendList.map(friend => (
						<StyledLink to={`/profile/${friend.id}`} key={friend.id}>
							<StyledDiv key={friend.id}>
								<StyledSpan>{friend.username}</StyledSpan>
								<StyledMessageBtn
									type='button'
									value='쪽지'
									onClick={e => {
										e.preventDefault();
										if (friend.id) {
											try {
												setPickedFriend(friend.id);
												setPickedFriendName(friend.firstname);
												setIsModalOn(true);
											} catch (error) {
												// console.log(error);
											}
										}
									}}
								>
									쪽지
								</StyledMessageBtn>
								<StyledDeleteBtn
									type='button'
									value='삭제'
									onClick={e => {
										e.preventDefault();
										if (friend.id) {
											try {
												apiDeleteFriend(friend.id.toString());
											} catch (error) {
												// console.log(error);
											}
										}
									}}
								>
									절교
								</StyledDeleteBtn>
							</StyledDiv>
						</StyledLink>
					))}
				{friendList.length === 0 && <StyledDiv> 없어요</StyledDiv>}
			</StyledContainer>
		</div>
	);
}

export default FriendList;
