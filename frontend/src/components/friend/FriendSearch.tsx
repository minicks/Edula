import React, { useEffect, useState } from 'react';
import styled from 'styled-components';
import { Link } from 'react-router-dom';
import StyledTitle from '../class/StyledTitle';
import { apigetSearchFriend, apiPostFriendRequest } from '../../api/friend';
import StyledDiv from './StyledDiv';
import StyledContainer from './StyledContainer';
import StyledDeleteBtn from './StyledDeleteBtn';

interface SearchDataType {
	studentCount: number;
	teacherCount: number;
	students: {
		id: number;
		username: string;
		firstName: string;
		friendRequest: string;
	}[];
	teachers: {
		id: number;
		username: string;
		firstName: string;
		friendRequest: string;
	}[];
}

const StyledBtn = styled(StyledDeleteBtn)`
	background: ${props => props.theme.pointColor};
	color: ${props => props.theme.fontColor};
	box-shadow: 0 1px 3px black;
`;
const SearchBtn = styled(StyledDeleteBtn)`
	background: ${props => props.theme.pointColor};
	color: ${props => props.theme.fontColor};
	box-shadow: 0 1px 3px black;
`;

const StyledLink = styled(Link)`
	text-decoration: none;
	font-size: 1em;
	color: ${props => props.theme.fontColor};
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

function FriendSearch() {
	const [searchResult, setSearchResult] = useState({} as SearchDataType);
	const [keyword, setKeyword] = useState('');

	const inputRef: React.RefObject<HTMLInputElement> = React.createRef();

	const getData = (event: React.FormEvent<EventTarget>) => {
		event.preventDefault();
		if (inputRef.current) {
			setKeyword(inputRef.current.value);
			inputRef.current.value = '';
		}
	};

	const getSearchResult = () => {
		apigetSearchFriend(keyword).then(res => {
			setSearchResult(res.data);
		});
	};

	useEffect(() => {
		if (keyword) {
			getSearchResult();
		}
	}, [keyword]);

	return (
		<div>
			<StyledContainer>
				<StyledTitle>친구 검색</StyledTitle>
				<StyledInput
					type='text'
					ref={inputRef}
					placeholder='친구 이름을 써보세요'
					onKeyPress={event => {
						if (event.key === 'Enter') {
							getData(event);
						}
					}}
				/>
				<SearchBtn type='button' onClick={getData}>
					검색
				</SearchBtn>

				{searchResult.students &&
					searchResult.students.map(friend => (
						<StyledDiv key={friend.id}>
							<StyledLink to={`/profile/${friend.id}`}>
								{friend.username} : {friend.firstName}
							</StyledLink>
							{!friend.friendRequest && (
								<StyledBtn
									type='button'
									value='친구 신청'
									onClick={e => {
										e.preventDefault();

										apiPostFriendRequest(friend.id.toString())
											.then(() => {
												window.location.reload();
											})
											.catch(() => {});
									}}
								>
									친구 신청
								</StyledBtn>
							)}
						</StyledDiv>
					))}
				{searchResult.studentCount === 0 && (
					<StyledDiv>검색 결과가 없어요. </StyledDiv>
				)}
			</StyledContainer>
		</div>
	);
}

export default FriendSearch;
