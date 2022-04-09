import styled from 'styled-components';

const SButton = styled.input`
	color: ${props => props.theme.fontColor};
	padding: 3px;
	border-radius: 3px;
	font-size: 1rem;
	width: 100%;
	background-color: ${props => props.theme.bgColor};

	&:hover {
		opacity: 0.9;
	}
	&:active {
		opacity: 1;
		box-shadow: 0px 0px 3px ${props => props.theme.bgColor};
	}
	&:disabled {
		opacity: 0.3;
	}
`;

type PropType = {
	value: string;
	disabled: boolean;
};

function FormBtn({ value, disabled }: PropType) {
	return <SButton type='submit' value={value} disabled={disabled} />;
}

export default FormBtn;
