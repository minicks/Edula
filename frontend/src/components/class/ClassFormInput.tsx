import styled from 'styled-components';

const ClassFormInput = styled.label`
	display: flex;

	& > * {
		box-sizing: border-box;
		border: 1px solid black;
		padding: 20px;
		font-size: 1rem;
	}

	input {
		width: 100%;
	}
`;

export default ClassFormInput;
