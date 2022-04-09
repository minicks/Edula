import styled from 'styled-components';

export const STel = styled.div`
	padding: 0.25em;
	font-size: 1em;
	border-bottom: 1px solid rgba(0, 0, 0, 0.3);
	width: 130px;
	min-height: 20px;
	text-align: center;
`;

type PropType = {
	value: string | number;
};

function Tel({ value }: PropType) {
	return <STel>{value}</STel>;
}

export default Tel;
