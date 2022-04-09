import { useEffect, useState } from 'react';
import styled from 'styled-components';
import { Link } from 'react-router-dom';
import StyledTitle from '../class/StyledTitle';
import {
	apiDeleteFriendRequest,
	apiGetFriendRequestList,
	apiPutFriendRequest,
} from '../../api/friend';
import StyledDiv from './StyledDiv';
import StyledContainer from './StyledContainer';
import StyledDeleteBtn from './StyledDeleteBtn';

interface FriendRequestDataType {
	requsetSend: {
		id: number;
		fromUser: {
			firstName: string;
			id: number;
			status: string;
			username: string;
		};
		toUser: {
			firstName: string;
			id: number;
			status: string;
			username: string;
		};
		requestStatus: string;
	}[];
	requsetReceive: {
		id: number;
		fromUser: {
			firstName: string;
			id: number;
			status: string;
			username: string;
		};
		toUser: {
			firstName: string;
			id: number;
			status: string;
			username: string;
		};
		requestStatus: string;
	}[];
}
const StyledSpan = styled.span`
	color: ${props => props.theme.fontColor};
`;
const StyledWaitingBtn = styled(StyledDeleteBtn)`
	background: ${props => props.theme.pointColor};
	color: ${props => props.theme.fontColor};
	box-shadow: 0 1px 3px black;
`;
const StyleAcceptBtn = styled(StyledDeleteBtn)`
	background: ${props => props.theme.borderColor};
	color: ${props => props.theme.fontColor};
	box-shadow: 0 1px 3px black;
`;
const StyleRefuseBtn = styled(StyledDeleteBtn)`
	background: ${props => props.theme.bgColor};
	color: ${props => props.theme.fontColor};
	box-shadow: 0 1px 3px black;
`;

const StyledLink = styled(Link)`
	text-decoration: none;
	font-size: 1em;
	color: ${props => props.theme.fontColor};
`;

function FriendRequest() {
	const [friendRequestList, setFriendRequestList] = useState(
		{} as FriendRequestDataType
	);

	const getFriendRequestList = () => {
		apiGetFriendRequestList().then(res => {
			setFriendRequestList(res.data);
		});
	};

	useEffect(() => {
		getFriendRequestList();
	}, []);

	return (
		<div>
			<StyledContainer>
				<StyledTitle>받은 친구 신청</StyledTitle>
				{friendRequestList.requsetReceive &&
					friendRequestList.requsetReceive.map(request => (
						<StyledDiv key={request.id}>
							<StyledLink to={`/profile/${request.fromUser?.id}`}>
								<StyledSpan key={request.id}>
									{request.fromUser?.username}: {request.fromUser?.firstName}
								</StyledSpan>
							</StyledLink>
							<StyleAcceptBtn
								onClick={e => {
									e.preventDefault();
									if (request.id) {
										try {
											apiPutFriendRequest(request.id.toString(), 'AC');
											window.location.reload();
										} catch (error) {
											// console.log(error);
										}
									}
								}}
							>
								수락
							</StyleAcceptBtn>

							<StyleRefuseBtn
								onClick={e => {
									e.preventDefault();
									if (request.id) {
										try {
											apiPutFriendRequest(request.id.toString(), 'RF');
											window.location.reload();
										} catch (error) {
											// console.log(error);
										}
									}
								}}
							>
								거부
							</StyleRefuseBtn>
						</StyledDiv>
					))}
				{friendRequestList.requsetReceive?.length === 0 && (
					<StyledDiv> 없어요.</StyledDiv>
				)}
			</StyledContainer>
			<StyledContainer>
				<StyledTitle>보낸 친구 신청</StyledTitle>
				{friendRequestList.requsetSend &&
					friendRequestList.requsetSend.map(request => (
						<StyledDiv key={request.id}>
							<StyledLink to={`/profile/${request.toUser}`}>
								<StyledSpan key={request.id}>
									{request.toUser?.username}: {request.toUser?.firstName}
								</StyledSpan>
							</StyledLink>

							<StyledWaitingBtn
								onClick={e => {
									e.preventDefault();
									if (request.id) {
										try {
											apiDeleteFriendRequest(request.id.toString());
											window.location.reload();
										} catch (error) {
											// console.log(error);
										}
									}
								}}
							>
								친구 신청 취소
							</StyledWaitingBtn>
						</StyledDiv>
					))}
				{friendRequestList.requsetSend?.length === 0 && (
					<StyledDiv> 없어요.</StyledDiv>
				)}
			</StyledContainer>
		</div>
	);
}

export default FriendRequest;
