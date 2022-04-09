import { SubmitErrorHandler, SubmitHandler, useForm } from 'react-hook-form';
import { useNavigate, useParams } from 'react-router-dom';
import FormBtn from '../auth/FormBtn';
import { apiPostHomework, apiUpdateHomework } from '../../api/homework';
import ClassFormInput from './ClassFormInput';

type ArticleInput = {
	title: string;
	content: string;
	deadline: string;
};

interface InnerProps {
	type: string;
	originTitle: string;
	originContent: string;
	originDeadline: string;
}

function HomeworkForm(props: InnerProps) {
	const { lectureId, homeworkId } = useParams();
	const { type, originTitle, originContent, originDeadline } = props;
	const {
		register,
		handleSubmit,
		formState: { isValid },
		getValues,
	} = useForm<ArticleInput>({
		mode: 'all',
	});

	const navigate = useNavigate();

	const onValidCreate: SubmitHandler<ArticleInput> = async () => {
		const { title, content, deadline } = getValues();

		if (lectureId) {
			try {
				await apiPostHomework(lectureId, title, content, deadline)
					.then(() => {})
					.catch(() => {
						// console.log(err);
					});

				navigate(`/lecture/${lectureId}`);
			} catch (error) {
				// console.log(error);
			}
		}
	};

	const onValidUpdate: SubmitHandler<ArticleInput> = async () => {
		const { title, content, deadline } = getValues();

		if (homeworkId && lectureId) {
			try {
				await apiUpdateHomework(lectureId, homeworkId, title, content, deadline)
					.then(() => {})
					.catch(() => {});
				navigate(`/lecture/${lectureId}`);
			} catch (error) {
				// console.log(error);
			}
		}
	};

	const onInValidSubmit: SubmitErrorHandler<ArticleInput> = () => {
		// error handling
	};

	return (
		<form
			onSubmit={handleSubmit(
				type === 'update' ? onValidUpdate : onValidCreate,
				onInValidSubmit
			)}
		>
			<ClassFormInput htmlFor='title'>
				<div>제목</div>
				<input
					{...register('title', {
						required: '제목을 입력하세요',
						minLength: {
							value: 1,
							message: '제목은 한 글자 이상 입력해주세요.',
						},
						maxLength: {
							value: 100,
							message: '제목은 백 글자 이하로 입력해주세요.',
						},
					})}
					type='text'
					placeholder='Title'
					defaultValue={originTitle}
				/>
			</ClassFormInput>

			<ClassFormInput htmlFor='content'>
				<div>내용</div>
				<input
					{...register('content', {
						required: '내용을 입력하세요.',
						minLength: {
							value: 1,
							message: '내용은 1글자 이상 1000글자 이하입니다.',
						},
						maxLength: {
							value: 500,
							message: '내용은 1글자 이상 500글자 이하입니다.',
						},
					})}
					type='text'
					placeholder='Content'
					defaultValue={originContent}
				/>
			</ClassFormInput>
			<ClassFormInput htmlFor='deadline'>
				<div>마감일</div>
				<input
					{...register('deadline', {
						required: '마감일을 정하세요.',
					})}
					type='datetime-local'
					placeholder='deadline'
					defaultValue={originDeadline}
				/>
			</ClassFormInput>
			{type === 'new' && <FormBtn value='글쓰기' disabled={!isValid} />}
			{type === 'update' && <FormBtn value='수정하기' disabled={!isValid} />}
		</form>
	);
}

export default HomeworkForm;
