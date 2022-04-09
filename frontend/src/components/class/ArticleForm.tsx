import { useContext } from 'react';
import { SubmitErrorHandler, SubmitHandler, useForm } from 'react-hook-form';
import { useNavigate, useParams } from 'react-router-dom';
import { apiPostArticle, apiUpdateArticle } from '../../api/article';
import FormBtn from '../auth/FormBtn';
import ClassFormInput from './ClassFormInput';

import UserContext from '../../context/user';

type ArticleInput = {
	title: string;
	content: string;
	notice: boolean;
};

interface InnerProps {
	type: string;
	originTitle: string;
	originContent: string;
	originNotice: boolean;
}

function ArticleForm(props: InnerProps) {
	const { userId } = useContext(UserContext);
	const { lectureId, articleId } = useParams();
	const { type, originTitle, originContent } = props;
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
		const { title, content, notice } = getValues();

		if (lectureId) {
			try {
				await apiPostArticle(
					lectureId,
					title,
					content,
					notice,
					userId.toString(),
					lectureId
				)
					.then(() => {})
					.catch(() => {});
				navigate(`/lecture/${lectureId}`);
			} catch (error) {
				// console.log(error);
			}
		}
	};

	const onValidUpdate: SubmitHandler<ArticleInput> = async () => {
		const { title, content, notice } = getValues();

		if (articleId && lectureId) {
			try {
				await apiUpdateArticle(
					lectureId,
					articleId,
					title,
					content,
					notice,
					userId.toString(),
					lectureId
				)
					.then(() => {})
					.catch(() => {
						// console.log(err);
					});
				navigate(`/${lectureId}/article/${articleId}`);
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
					placeholder='당신은 우리 학교의 자랑❤'
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
					placeholder='예쁜 글을 써주세요 :)'
					defaultValue={originContent}
				/>
			</ClassFormInput>
			<ClassFormInput htmlFor='notice'>
				<div>공지 여부</div>
				<input {...register('notice', {})} type='checkbox' placeholder='notice' />
			</ClassFormInput>
			{type === 'new' && <FormBtn value='글쓰기' disabled={!isValid} />}
			{type === 'update' && <FormBtn value='수정하기' disabled={!isValid} />}
		</form>
	);
}

export default ArticleForm;
