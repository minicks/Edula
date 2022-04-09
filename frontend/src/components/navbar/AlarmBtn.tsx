import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { AiFillBell } from 'react-icons/ai';
import styled, { css } from 'styled-components';
import { apiGetNotificationCnt } from '../../api/notice';

interface InnerAlarm {
	alarmCnt: string;
}

const StyledAlarmBtn = styled.span<InnerAlarm>`
	width: 30px;
	margin-right: 20px;
	height: inherit;
	color: white;
	display: flex;
	justify-content: center;
	align-items: center;
	position: relative;

	${props =>
		props.alarmCnt !== '0' &&
		css`
			color: yellow;
			::after {
				content: '${props.alarmCnt}';
				min-width: 20px;
				height: 20px;
				background-color: ${props.theme.pointColor};
				font-weight: bolt;
				font-size: 14px;
				display: flex;
				justify-content: center;
				align-items: center;
				border-radius: 50%;
				position: absolute;
				top: 5px;
				right: 5px;
				transition: 0.3s;
				opacity: 0;
				transform: scale(0.5);
				will-change: opacity, transform;
				opacity: 1;
				transform: scale(1);
			}
		`}
`;

const StyledSpan = styled.span`
	display: flex;
`;

function Alarm() {
	const [alarmCnt, setAlarmCnt] = useState(0);
	useEffect(() => {
		apiGetNotificationCnt().then(res => {
			setAlarmCnt(res.data?.count);
		});
	}, []);

	return (
		<StyledSpan>
			<Link to='/alarm'>
				<StyledAlarmBtn alarmCnt={alarmCnt > 9 ? '9+' : alarmCnt.toString()}>
					<AiFillBell />
				</StyledAlarmBtn>
			</Link>
		</StyledSpan>
	);
}

export default Alarm;
