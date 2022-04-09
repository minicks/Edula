import { useContext, useState, useEffect } from 'react';
import styled from 'styled-components';
import { useParams, Link } from 'react-router-dom';
import HomeworkSubmitForm from '../components/class/HomeworkSubmitForm';
import UserContext from '../context/user';
import {
	apiGetHomeworkSubmission,
	apiDeleteHomeworkSubmission,
} from '../api/homework';
import StyledTitle from '../components/class/StyledTitle';
import StyledContainer from '../components/friend/StyledContainer';
import StyledDeleteBtn from '../components/friend/StyledDeleteBtn';
import StyledContent from '../components/class/StyledContent';
import PageTitle from '../components/PageTitle';

const StyledListItem = styled.li`
	font-size: 1em;
	text-align: center;
	margin: 1em;
	background: ${props => props.theme.bgColor};
	padding: 1em 2em 1em 2em;
	box-shadow: 0 1px 1px rgba(0, 0, 0, 0.125);
	border-radius: 10px;
`;
const StyledUpContainer = styled.div`
	display: flex;
	flex-direction: column;
	justify-content: center;
	align-items: center;
	width: 100%;
	margin: 20px;
`;

const StyledSubmitNotification = styled(StyledContent)`
	font-size: 1rem;
	padding: 0.1rem 0.1rem;
	background: ${props => props.theme.subBgColor};
`;
interface submissionHomeworkData {
	id: number;
	title: string;
	content: string;
	createAt: string;
	homework: number;
	writer: number;
}

const StyledLink = styled(Link)`
	text-decoration: none;
	font-size: 1em;
	color: ${props => props.theme.fontColor};
`;

function HomeworkSubmit() {
	const { userStat, userId } = useContext(UserContext);
	const { lectureId, homeworkId } = useParams();
	const [submissionList, setSubmissionList] = useState(
		[] as submissionHomeworkData[]
	);
	const [isSubmit, setIsSubmit] = useState(false);

	if (lectureId && homeworkId) {
		useEffect(() => {
			if (userStat === 'ST') {
				apiGetHomeworkSubmission(lectureId, homeworkId)
					.then(res => {
						if (res.status === 204) {
							setIsSubmit(false);
						} else {
							setIsSubmit(true);
						}
					})
					.catch(() => {});
			} else {
				apiGetHomeworkSubmission(lectureId, homeworkId)
					.then(res => {
						setSubmissionList(res.data);
					})
					.catch(() => {});
			}
		}, [isSubmit]);
	}

	if (userStat === 'ST') {
		return (
			<StyledUpContainer>
				<StyledTitle>과제 제출 💌</StyledTitle>

				{isSubmit === true ? (
					<StyledSubmitNotification>
						과제 제출함!{' '}
						<StyledDeleteBtn
							type='button'
							value='삭제'
							onClick={e => {
								e.preventDefault();
								if (lectureId && homeworkId) {
									try {
										apiDeleteHomeworkSubmission(lectureId, homeworkId, userId)
											.then(() => {
												setIsSubmit(false);
											})
											.catch(() => {});
									} catch (error) {
										// console.log(error);
									}
								}
							}}
						>
							삭제
						</StyledDeleteBtn>
					</StyledSubmitNotification>
				) : (
					<StyledSubmitNotification>과제 제출 안함!</StyledSubmitNotification>
				)}

				<HomeworkSubmitForm isSubmit={isSubmit} />
			</StyledUpContainer>
		);
	}
	return (
		<StyledContainer>
			<PageTitle title='과제 제출' />
			<StyledTitle>과제 제출 현황</StyledTitle>
			<ul>
				{submissionList &&
					submissionList?.map(submission => (
						<StyledLink
							key={submission.id}
							to={`/${lectureId}/homework/${homeworkId}/submit/${submission.writer}`}
						>
							<StyledListItem key={submission.id}>
								{submission.writer}번 학생
							</StyledListItem>
						</StyledLink>
					))}
			</ul>
		</StyledContainer>
	);
}

export default HomeworkSubmit;
