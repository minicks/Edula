import styled from 'styled-components';

const FormInput = styled.label`
	display: flex;

	& > * {
		box-sizing: border-box;
		border: 1px solid black;
		padding: 8px;
		font-size: 1rem;
		border-radius: 3px;
	}

	input {
		width: 100%;
		border-radius: 3px;
		padding: 5px;
	}
`;

export default FormInput;
