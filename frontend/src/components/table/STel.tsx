import styled from 'styled-components';
import { STel } from './Tel';

const SmallSTel = styled(STel)`
	width: 50px;
`;

type PropType = {
	value: string | number;
};

function SmallTel({ value }: PropType) {
	return <SmallSTel>{value}</SmallSTel>;
}

export default SmallTel;
