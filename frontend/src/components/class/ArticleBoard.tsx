import { useEffect, useState } from 'react';
import styled from 'styled-components';
import { Link, useParams } from 'react-router-dom';
import StyledTitle from './StyledTitle';
import StyledButton from './StyledButton';
import { apiGetArticles } from '../../api/article';
import Pagination from './ArticlePagination';

const StyledListItem = styled.li`
	font-size: 1em;
	text-align: center;
	margin: 1em;
	background: ${props => props.theme.subBgColor};
	color: ${props => props.theme.fontColor};
	padding: 1em 1em 1em 2em;
	border-left: 4px solid #ddd;
	box-shadow: 0 1px 1px rgba(0, 0, 0, 0.125);
	border-radius: 10px;
`;

const StyledLink = styled(Link)`
	text-decoration: none;
	font-size: 1em;
`;
const StyledContainer = styled.div`
	margin: 0 3em;
`;
interface ArticleDataType {
	content: string;
	createdAt: string;
	id: number;
	lecture: number;
	notice: boolean;
	title: string;
	writer: number;
	updatedAt: string;
}

function ArticleBoard() {
	const { lectureId } = useParams();
	const [articles, setArticleData] = useState([] as ArticleDataType[]);
	const [limit, setLimit] = useState(10);
	const [page, setPage] = useState(1);
	const [total, setTotal] = useState(0);

	const getArticles = () => {
		if (lectureId) {
			apiGetArticles(lectureId, page.toString(), limit.toString()).then(res => {
				setTotal(res.data.totlaCount);
				setArticleData(res.data.articles);
			});
		}
	};

	useEffect(() => {
		getArticles();
	}, [page, limit]);

	if (articles) {
		return (
			<StyledContainer>
				<StyledTitle>게시판</StyledTitle>

				{articles.length !== 0 && (
					<label htmlFor='limit'>
						페이지 당 표시할 게시물 수:&nbsp;
						<select
							value={limit}
							onChange={({ target: { value } }) => setLimit(Number(value))}
						>
							<option value='5'>5</option>
							<option value='10'>10</option>
							<option value='12'>12</option>
							<option value='20'>20</option>
						</select>
					</label>
				)}

				<ul>
					{articles &&
						articles.map(article => (
							<StyledLink to={`/${lectureId}/article/${article.id}`} key={article.id}>
								<StyledListItem>
									<h1>{article.title}</h1>
									<p>{article.content}</p>
								</StyledListItem>
							</StyledLink>
						))}
				</ul>
				{articles.length === 0 && <StyledTitle>게시글이 없어요..</StyledTitle>}
				<Link to={`/${lectureId}/articleCreate`}>
					<StyledButton>글쓰기</StyledButton>
				</Link>

				{articles.length !== 0 && (
					<footer>
						<Pagination total={total} limit={limit} page={page} setPage={setPage} />
					</footer>
				)}
			</StyledContainer>
		);
	}
	return <h1>로딩 중</h1>;
}

export default ArticleBoard;
