import { useContext, useEffect, useState } from 'react';
import { SubmitErrorHandler, SubmitHandler, useForm } from 'react-hook-form';
import { useParams, useNavigate } from 'react-router-dom';
import {
	apiGetHomeworkSubmissionDetail,
	apiPostHomeworkSubmission,
} from '../../api/homework';
import UserContext from '../../context/user';
import FormBtn from '../auth/FormBtn';
import FormInput from '../auth/FormInput';

interface HomeworkData {
	title: string;
	content: string;
	file: FileList;
	homework: string;
	writer: string;
}

interface Props {
	isSubmit: boolean;
}
function HomeworkSubmitForm({ isSubmit }: Props) {
	const { userId } = useContext(UserContext);
	const { lectureId, homeworkId } = useParams();
	const [data, setData] = useState({} as HomeworkData);
	const {
		register,
		handleSubmit,
		formState: { isValid },
		getValues,
	} = useForm<HomeworkData>({
		mode: 'all',
	});
	const navigate = useNavigate();

	const onValidCreate: SubmitHandler<HomeworkData> = async () => {
		const { title, content, file } = getValues();

		if (lectureId && homeworkId) {
			const formData = new FormData();

			for (let i = 0; i < file.length; i += 1) {
				formData.append(`file${i}`, file[i]);
			}

			formData.append('enctype', 'multipart/form-data');
			formData.append('title', title);
			formData.append('content', content);
			formData.append('userId', userId);
			try {
				await apiPostHomeworkSubmission(lectureId, homeworkId, formData)
					.then(() => {})
					.catch(() => {});
				navigate(`/lecture/${lectureId}`);
			} catch (error) {
				// console.log(error);
			}
		}
	};

	const onInValidSubmit: SubmitErrorHandler<HomeworkData> = () => {
		// error handling
	};

	if (lectureId && homeworkId) {
		useEffect(() => {
			apiGetHomeworkSubmissionDetail(lectureId, homeworkId, userId)
				.then(res => {
					setData(res.data);
				})
				.catch(() => {});
		}, []);
	}
	if (isSubmit) {
		if (data) {
			return (
				<form onSubmit={handleSubmit(onValidCreate, onInValidSubmit)}>
					<FormInput htmlFor='title'>
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
							placeholder='??????'
							defaultValue={data.title}
						/>
					</FormInput>

					<FormInput htmlFor='content'>
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
							placeholder='??????'
							defaultValue={data.content}
						/>
					</FormInput>
					<FormInput htmlFor='file'>
						<div>??????</div>
						<input
							{...register('file', {})}
							type='file'
							multiple
							placeholder='file'
						/>
					</FormInput>
					<FormBtn value='?????? ??????' disabled={!isValid} />
				</form>
			);
		}
		return <h1>?????? ???!</h1>;
	}
	return (
		<form onSubmit={handleSubmit(onValidCreate, onInValidSubmit)}>
			<FormInput htmlFor='title'>
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
					placeholder='Title'
				/>
			</FormInput>

			<FormInput htmlFor='content'>
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
					placeholder='Content'
				/>
			</FormInput>
			<FormInput htmlFor='file'>
				<div>??????</div>
				<input {...register('file', {})} type='file' multiple placeholder='file' />
			</FormInput>
			<FormBtn value='?????? ??????' disabled={!isValid} />
		</form>
	);
}

export default HomeworkSubmitForm;
