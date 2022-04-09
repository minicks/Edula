import styled from 'styled-components';
import { BiErrorCircle } from 'react-icons/bi';

const SErrorMsg = styled.div`
	box-sizing: border-box;
	border: 1px solid ${props => props.theme.warningColor};
	border-radius: 3px;
	padding: 3px;
	margin: 3px 0px;
	color: ${props => props.theme.fontColor};
	font-size: 12px;
`;

const ErrorIcon = styled(BiErrorCircle)`
	color: ${props => props.theme.warningColor};
	margin-right: 3px;
`;

type PropType = {
	message: string;
};

function ErrorMsg({ message }: PropType) {
	return (
		<SErrorMsg>
			<ErrorIcon />
			{message}
		</SErrorMsg>
	);
}

export default ErrorMsg;
