import { AxiosError } from 'axios';
import { useForm } from 'react-hook-form';
import { useNavigate } from 'react-router-dom';
import { apiPostProfileImg } from '../../api/user';
import Btn from '../../common/Btn';
import routes from '../../routes';
import FormBox from '../auth/FormBox';
import FormBtn from '../auth/FormBtn';
import FormInput from '../auth/FormInput';

type EditImgInput = {
	result: string;
	profileImage: File;
};

type PropType = {
	toggleMode: (mode: string) => void;
};

function EditImgForm({ toggleMode }: PropType) {
	const {
		register,
		handleSubmit,
		formState: { errors },
		getValues,
		clearErrors,
	} = useForm<EditImgInput>({
		mode: 'all',
	});
	const navigate = useNavigate();

	const onValidSubmit = async () => {
		const { profileImage } = getValues();
		const formData = new FormData();
		formData.append('profileImage', profileImage);
		formData.append('enctype', 'multipart/form-data');
		try {
			await apiPostProfileImg(formData).then(res => console.log(res));
			toggleMode('profile');
		} catch (e) {
			const error = e as AxiosError;
			if (error?.response?.status === 401) {
				navigate(routes.login);
			}
		}
	};

	return (
		<FormBox>
			<form onSubmit={handleSubmit(onValidSubmit)}>
				<FormInput htmlFor='profileImage'>
					<input
						{...register('profileImage')}
						type='file'
						placeholder='새 프로필 사진'
					/>
				</FormInput>
				<FormBtn value='수정' disabled={false} />
				<Btn onClick={() => toggleMode('profile')}>취소</Btn>
			</form>
		</FormBox>
	);
}

export default EditImgForm;
