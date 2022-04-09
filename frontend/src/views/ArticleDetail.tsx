import { useEffect, useState, useContext } from 'react';
import { useParams, Link, useNavigate } from 'react-router-dom';
import styled from 'styled-components';
import StyledTitle from '../components/class/StyledTitle';
import StyledContent from '../components/class/StyledContent';
import StyledButton from '../components/class/StyledButton';
import { apiGetArticleDetail, apiDeleteArticle } from '../api/article';
import UserContext from '../context/user';
import StyledDeleteBtn from '../components/friend/StyledDeleteBtn';
import PageTitle from '../components/PageTitle';

const StyledContainer = styled.div`
	display: flex;
	flex-direction: column;
	justify-content: center;
	align-items: center;
	margin: 20px;
	font-size: 1em;
	text-align: center;
	border: solid 2px ${props => props.theme.subBgColor};
	color: ${props => props.theme.fontColor};
	padding: 1em 1em 1em 2em;
	box-shadow: 0 1px 1px rgba(0, 0, 0, 0.125);
	border-radius: 10px;
`;

const StyleUpdateBtn = styled(StyledDeleteBtn)`
	background: ${props => props.theme.borderColor};
	color: ${props => props.theme.fontColor};
	box-shadow: 0 1px 3px black;
`;
const StyleDeleteBtn = styled(StyledDeleteBtn)`
	background: ${props => props.theme.warningColor};
	color: ${props => props.theme.fontColor};
	box-shadow: 0 1px 3px black;
`;
const StyleSubmitBtn = styled(StyledDeleteBtn)`
	background: ${props => props.theme.subBgColor};
	color: ${props => props.theme.fontColor};
	box-shadow: 0 1px 3px black;
`;
const StyledLink = styled(Link)`
	text-decoration: none;
	font-size: 1em;
	color: ${props => props.theme.fontColor};
`;

interface ArticleDataType {
	content: string;
	createdAt: string;
	notice: boolean;
	id: number;
	lecture: number;
	title: string;
	writer: {
		id: number;
		username: string;
		firstName: string;
		status: string;
	};
	updatedAt: string;
}

function ArticleDetail() {
	const { userId } = useContext(UserContext);
	const { lectureId, articleId } = useParams();
	const navigate = useNavigate();

	const [articleData, setArticleData] = useState({} as ArticleDataType);

	if (articleId && lectureId) {
		useEffect(() => {
			apiGetArticleDetail(lectureId, articleId).then(res => {
				setArticleData(res.data);
			});
		}, []);
	}

	return (
		<StyledContainer>
			<PageTitle title={articleData.title} />
			<StyledTitle>{articleData.title}</StyledTitle>
			<StyledContent>
				글쓴 날: {articleData.createdAt?.slice(0, 10)}/ 최종 수정일:{' '}
				{articleData.updatedAt?.slice(0, 10)}
			</StyledContent>
			<StyledContent>글쓴이: {articleData.writer?.username}</StyledContent>
			<StyledContent>{articleData.content}</StyledContent>
			{articleData.writer?.id === parseInt(userId, 10) && (
				<div>
					<StyledLink to={`/${lectureId}/articleUpdate/${articleId}`}>
						<StyleUpdateBtn>수정</StyleUpdateBtn>
					</StyledLink>
					<StyleDeleteBtn
						type='button'
						value='삭제'
						onClick={e => {
							e.preventDefault();
							if (articleId && lectureId) {
								try {
									apiDeleteArticle(lectureId, articleId)
										.then(() => {})
										.catch(() => {});

									navigate(`/lecture/${lectureId}`);
								} catch (error) {
									// console.log(error);
								}
							}
						}}
					>
						삭제
					</StyleDeleteBtn>
					<StyledLink to={`/lecture/${lectureId}/`}>
						<StyleSubmitBtn>목록</StyleSubmitBtn>
					</StyledLink>
				</div>
			)}
			{articleData.writer?.id !== parseInt(userId, 10) && (
				<StyledLink to={`/lecture/${lectureId}/`}>
					<StyleSubmitBtn>목록</StyleSubmitBtn>
				</StyledLink>
			)}
		</StyledContainer>
	);
}

export default ArticleDetail;
