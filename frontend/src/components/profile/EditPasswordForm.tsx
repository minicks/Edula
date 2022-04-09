import { AxiosError } from 'axios';
import { useForm } from 'react-hook-form';
import { BiUser } from 'react-icons/bi';
import { useNavigate } from 'react-router-dom';
import { apiChangePassword } from '../../api/user';
import Btn from '../../common/Btn';
import routes from '../../routes';
import FormBox from '../auth/FormBox';
import FormBtn from '../auth/FormBtn';
import FormInput from '../auth/FormInput';

type EditPasswordInput = {
	result: string;
	oldPassword: string;
	newPassword: string;
	newPasswordConfirmation: string;
};

type PropType = {
	toggleMode: (mode: string) => void;
};

function EditPasswordForm({ toggleMode }: PropType) {
	const {
		register,
		handleSubmit,
		formState: { errors },
		getValues,
		clearErrors,
	} = useForm<EditPasswordInput>({
		mode: 'all',
	});
	const navigate = useNavigate();

	const onValidSubmit = async () => {
		const { oldPassword, newPassword, newPasswordConfirmation } = getValues();

		try {
			await apiChangePassword(oldPassword, newPassword, newPasswordConfirmation);
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
				<FormInput htmlFor='oldPassword'>
					<span>
						<BiUser />
					</span>
					<input
						{...register('oldPassword', {
							required: '비밀번호를 입력하세요.',
							minLength: {
								value: 8,
								message: '비밀번호는 8자 이상, 16자 이하입니다.',
							},
							maxLength: {
								value: 16,
								message: '비밀번호는 8자 이상, 16자 이하입니다.',
							},
						})}
						type='password'
						placeholder='기존 비밀번호'
						onInput={() => clearErrors()}
					/>
				</FormInput>
				<FormInput htmlFor='newPassword'>
					<span>
						<BiUser />
					</span>
					<input
						{...register('newPassword', {
							required: '비밀번호를 입력하세요.',
							minLength: {
								value: 8,
								message: '비밀번호는 8자 이상, 16자 이하입니다.',
							},
							maxLength: {
								value: 16,
								message: '비밀번호는 8자 이상, 16자 이하입니다.',
							},
						})}
						type='password'
						placeholder='새 비밀번호'
						onInput={() => clearErrors()}
					/>
				</FormInput>
				<FormInput htmlFor='newPasswordConfirmation'>
					<span>
						<BiUser />
					</span>
					<input
						{...register('newPasswordConfirmation', {
							required: '비밀번호를 입력하세요.',
							minLength: {
								value: 8,
								message: '비밀번호는 8자 이상, 16자 이하입니다.',
							},
							maxLength: {
								value: 16,
								message: '비밀번호는 8자 이상, 16자 이하입니다.',
							},
						})}
						type='password'
						placeholder='새 비밀번호 확인'
						onInput={() => clearErrors()}
					/>
				</FormInput>
				<FormBtn value='수정' disabled={false} />
				<Btn onClick={() => toggleMode('profile')}>취소</Btn>
			</form>
		</FormBox>
	);
}

export default EditPasswordForm;
