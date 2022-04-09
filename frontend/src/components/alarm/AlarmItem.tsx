import { useState } from 'react';
import styled, { css } from 'styled-components';
import { Link } from 'react-router-dom';

interface Type {
	type: String;
}

const StyledLink = styled(Link)`
	text-decoration: none;
	font-size: 2em;
`;

const StyledContainer = styled.div<Type>`
	font-size: 1em;
	text-align: center;
	position: relative;
	margin: 2em;
	background: ${props => props.theme.subBgColor};
	padding: 1em 1em 1em 2em;
	border-left: 4px solid #ddd;
	box-shadow: 0 1px 1px rgba(0, 0, 0, 0.125);
	border-radius: 10px;

	:before {
		position: absolute;
		top: 50%;
		margin-top: -17px;
		left: -17px;
		background-color: #ddd;
		color: ${props => props.theme.subBgColor};
		width: 30px;
		height: 30px;
		border-radius: 100%;
		text-align: center;
		line-height: 30px;
		font-weight: bold;
		text-shadow: 1px 1px ${props => props.theme.fontColor};
	}

	${props =>
		props.type === '과제' &&
		css`
			border-color: ${props.theme.pointColor};
			:before {
				content: '과';
				background-color: ${props.theme.pointColor};
			border-color: ${props.theme.pointColor};
		
		`}

	${props =>
		props.type === '쪽지' &&
		css`
			border-color: ${props.theme.iconColorActive};
			:before {
				content: '쪽';
				background-color: ${props.theme.iconColorActive};
			border-color: ${props.theme.iconColorActive};
		
		`}
`;

const StyledContent = styled.div`
	margin: 1em;
`;

function AlarmItem() {
	const [alarms] = useState([
		{
			type: '과제',
			title: '수학 익힘책 19-20 페이지',
			content: '친구들 ^^ 수학 익힘책 풀어오세요~ ',
			author: '나담임',
			created_at: '2021.1.9',
			link: '',
		},
		{
			type: '쪽지',
			title: '안뇽',
			content:
				'안녕? 잘지내지? 다음 주에 내 생일 파티에 초대할게. 4시에 우리집으로 와',
			author: '나친구',
			created_at: '2021.1.15',
			link: '',
		},
	]);
	return (
		<div>
			<ul>
				{alarms.map(alarm => (
					<StyledContainer type={alarm.type} key={alarm.title}>
						<StyledLink to='/'>{alarm.title}</StyledLink>
						<StyledContent>
							{alarm.author}, {alarm.created_at}
						</StyledContent>
						<StyledContent>{alarm.content}</StyledContent>
					</StyledContainer>
				))}
			</ul>
		</div>
	);
}

export default AlarmItem;
