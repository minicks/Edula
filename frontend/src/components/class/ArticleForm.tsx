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
				<div>??????</div>
				<input
					{...register('title', {
						required: '????????? ???????????????',
						minLength: {
							value: 1,
							message: '????????? ??? ?????? ?????? ??????????????????.',
						},
						maxLength: {
							value: 100,
							message: '????????? ??? ?????? ????????? ??????????????????.',
						},
					})}
					type='text'
					placeholder='????????? ?????? ????????? ?????????'
					defaultValue={originTitle}
				/>
			</ClassFormInput>

			<ClassFormInput htmlFor='content'>
				<div>??????</div>
				<input
					{...register('content', {
						required: '????????? ???????????????.',
						minLength: {
							value: 1,
							message: '????????? 1?????? ?????? 1000?????? ???????????????.',
						},
						maxLength: {
							value: 500,
							message: '????????? 1?????? ?????? 500?????? ???????????????.',
						},
					})}
					type='text'
					placeholder='?????? ?????? ???????????? :)'
					defaultValue={originContent}
				/>
			</ClassFormInput>
			<ClassFormInput htmlFor='notice'>
				<div>?????? ??????</div>
				<input {...register('notice', {})} type='checkbox' placeholder='notice' />
			</ClassFormInput>
			{type === 'new' && <FormBtn value='?????????' disabled={!isValid} />}
			{type === 'update' && <FormBtn value='????????????' disabled={!isValid} />}
		</form>
	);
}

export default ArticleForm;
