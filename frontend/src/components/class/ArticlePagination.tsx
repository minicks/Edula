import styled from 'styled-components';

interface Props {
	total: number;
	limit: number;
	page: number;
	setPage: Function;
}
type ButtonProp = {
	onClick: Function;
};

const StyledButton = styled.button<ButtonProp>``;
function Pagination({ total, limit, page, setPage }: Props) {
	const numPages = Math.ceil(total / limit);

	return (
		<Nav>
			<Button onClick={() => setPage(page - 1)} disabled={page === 1}>
				&lt;
			</Button>
			{Array(numPages)
				.fill(page)
				.map((_, i) => (
					<Button
						type='button'
						// eslint-disable-next-line react/no-array-index-key
						key={i + 1}
						onClick={() => setPage(i + 1)}
						aria-current={page === i + 1 ? 'page' : undefined}
					>
						{i + 1}
					</Button>
				))}
			<Button onClick={() => setPage(page + 1)} disabled={page === numPages}>
				&gt;
			</Button>
		</Nav>
	);
}

const Nav = styled.nav`
	display: flex;
	justify-content: center;
	align-items: center;
	gap: 4px;
	margin: 16px;
`;

const Button = styled.button`
	border: none;
	border-radius: 8px;
	padding: 8px;
	margin: 0;
	background: ${props => props.theme.subBgColor};
	color: ${props => props.theme.fontColor};
	font-size: 1rem;

	&:hover {
		background: ${props => props.theme.warningColor};
		cursor: pointer;
		transform: translateY(-2px);
	}

	&[disabled] {
		background: grey;
		cursor: revert;
		transform: revert;
	}

	&[aria-current] {
		background: ${props => props.theme.pointColor};
		font-weight: bold;
		cursor: revert;
		transform: revert;
	}
`;

export default Pagination;
