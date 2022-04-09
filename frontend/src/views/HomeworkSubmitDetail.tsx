import { useEffect, useState } from 'react';
import { useParams, Link } from 'react-router-dom';
import { apiGetHomeworkSubmissionDetail } from '../api/homework';
import StyledTitle from '../components/class/StyledTitle';
import StyledContent from '../components/class/StyledContent';
import StyledContainer from '../components/schedule/StyledContainer';
import StyledButton from '../components/class/StyledButton';
import PageTitle from '../components/PageTitle';

interface HomeworkDataType {
	id: number;
	title: string;
	content: string;
	cretedAt: string;

	homeworkSubmissionFiles: {
		files: string;
		homeworkSubmission: number;
		id: number;
	}[];
	writer: number;
}

function HomeworkSubmitDetail() {
	const { lectureId, homeworkId, userId } = useParams();

	const [HomeworkData, setHomeworkData] = useState({} as HomeworkDataType);
	if (userId && lectureId && homeworkId) {
		useEffect(() => {
			apiGetHomeworkSubmissionDetail(lectureId, homeworkId, userId).then(res => {
				setHomeworkData(res.data);
			});
		}, []);
	}

	return (
		<StyledContainer>
			<PageTitle title={HomeworkData.title} />
			<StyledTitle>{HomeworkData.title}</StyledTitle>
			<StyledContent>{HomeworkData.writer}번 학생</StyledContent>
			<StyledContent>
				제출 시각: {HomeworkData.cretedAt?.slice(0, 10)}{' '}
				{HomeworkData.cretedAt?.slice(11, 19)}
			</StyledContent>
			<StyledContent>{HomeworkData.content}</StyledContent>
			<ul>
				{HomeworkData.homeworkSubmissionFiles?.length > 0 &&
					Array.from(Array(HomeworkData.homeworkSubmissionFiles?.length).keys()).map(
						i => (
							<li key={i}>
								<a
									href={`${process.env.REACT_APP_PROTOCOL}://${window.location.hostname}:${process.env.REACT_APP_PORT}${HomeworkData.homeworkSubmissionFiles[i]?.files}`}
									download
								>
									<StyledButton>과제 {i + 1}번 파일 다운로드</StyledButton>
								</a>
							</li>
						)
					)}
			</ul>

			<Link to={`/${lectureId}/homework/${homeworkId}/submit`}>
				<StyledButton>목록</StyledButton>
			</Link>
		</StyledContainer>
	);
}

export default HomeworkSubmitDetail;
