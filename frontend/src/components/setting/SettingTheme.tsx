import React, { useState, useEffect, useContext } from 'react';
import styled from 'styled-components';
import ThemeContext from '../../context/theme';

const StyledTitle = styled.h3`
	font-size: 1.5em;
	text-align: center;
	margin: 1em 1em;
	color: ${props => props.theme.fontColor};
`;
const StyledContainer = styled.div`
	display: flex;
	align-items: center;
	justify-content: center;
	color: ${props => props.theme.fontColor};
`;

const StyledSelect = styled.select`
	width: 150px;
	height: 35px;
	padding: 5px 30px 5px 10px;
	border-radius: 4px;
	outline: 0 none;
	background: ${props => props.theme.subBgColor};
	color: ${props => props.theme.bgColor};
	font-size: 16px;
`;
const StyledOption = styled.option`
	background: ${props => props.theme.subBgColor};
	color: ${props => props.theme.bgColor};
	padding: 3px 0;

	:hover {
		background: ${props => props.theme.fontColor};
	}
`;

function SettingTheme() {
	const [Selected, setSelected] = useState('');

	useEffect(() => {
		const theme = window.localStorage.getItem('theme');
		if (theme === 'dark') {
			document.getElementsByTagName('html')[0].classList.add('dark');
		}
	}, []);

	const { changeTheme } = useContext(ThemeContext);

	const handleChangeSelect = (event: React.ChangeEvent<HTMLSelectElement>) => {
		setSelected(event.target.value);
		changeTheme(event.target.value);
	};

	return (
		<StyledContainer>
			<StyledTitle>테마 :</StyledTitle>
			<StyledSelect value={Selected} onChange={event => handleChangeSelect(event)}>
				<StyledOption value='none'>Select Type</StyledOption>
				<StyledOption value='base'>밝은 테마</StyledOption>
				<StyledOption value='colorful'>알록달록</StyledOption>
				<StyledOption value='nature'>숲</StyledOption>
				<StyledOption value='twilight'>보랏빛 하늘</StyledOption>
				<StyledOption value='dark'>깜깜한 밤</StyledOption>
			</StyledSelect>
		</StyledContainer>
	);
}

export default SettingTheme;
