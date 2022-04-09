import styled from 'styled-components';
import { STel } from './Tel';

const MediumSTel = styled(STel)`
	width: 70px;
`;

type PropType = {
	value: string | number;
};

function MediumTel({ value }: PropType) {
	return <MediumSTel>{value}</MediumSTel>;
}

export default MediumTel;
