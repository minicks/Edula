import { SubmitHandler, useForm } from 'react-hook-form';
import { FaUserTag } from 'react-icons/fa';
import { VscMail } from 'react-icons/vsc';
import { ImEnter } from 'react-icons/im';
import { Link } from 'react-router-dom';
import styled from 'styled-components';
import { apiResetPassword } from '../../api/user';
import ErrorMsg from '../../components/auth/ErrorMsg';
import EmptyMsg from '../../components/auth/EmptyMsg';
import AuthLayout from '../../components/auth/AuthLayout';
import PageTitle from '../../components/PageTitle';
import FormBox from '../../components/auth/FormBox';
import FormInput from '../../components/auth/FormInput';
import FormBtn from '../../components/auth/FormBtn';
import LinkBox from '../../components/auth/LinkBox';
import routes from '../../routes';

const HeaderContainer = styled.div`
	width: 100%;
	padding: 30px 0px;
	display: flex;
	justify-content: center;
	align-items: center;

	h1 {
		font-size: 2rem;
		font-weight: 700;
	}
`;

type FindpwInput = {
	result: string;
	id: string;
	email: string;
};

function Findpw() {
	const {
		register,
		handleSubmit,
		formState: { errors, isValid },
		getValues,
		setError,
		clearErrors,
	} = useForm<FindpwInput>({ mode: 'all' });

	const onValidSubmit: SubmitHandler<FindpwInput> = async () => {
		const { id, email } = getValues();

		try {
			await apiResetPassword(id, email).then(res => console.log(res));
			alert('이메일로 새로운 비밀번호가 발송되었습니다.');
		} catch (e) {
			setError('result', { message: '사용자 정보가 일치하지 않습니다.' });
		}
	};

	const clearFindError = () => {
		clearErrors('result');
	};

	const resultError = errors.result?.message ? (
		<ErrorMsg message={errors.result?.message} />
	) : (
		<EmptyMsg />
	);

	const idError = errors.id?.message ? (
		<ErrorMsg message={errors.id?.message} />
	) : (
		<EmptyMsg />
	);

	const emailError = errors.email?.message ? (
		<ErrorMsg message={errors.email?.message} />
	) : (
		<EmptyMsg />
	);

	return (
		<AuthLayout>
			<PageTitle title='비밀번호 찾기' />
			<HeaderContainer>
				<h1>비밀번호 찾기</h1>
			</HeaderContainer>
			<FormBox>
				<form onSubmit={handleSubmit(onValidSubmit)}>
					{resultError}
					<FormInput htmlFor='id'>
						<span>
							<FaUserTag />
						</span>
						<input
							{...register('id', {
								required: '아이디를 입력하세요',
								minLength: {
									value: 8,
									message: '아이디는 8자 이상, 16자 이하입니다.',
								},
								maxLength: {
									value: 16,
									message: '아이디는 8자 이상, 16자 이하입니다.',
								},
								pattern: {
									value: /^[a-z]{2,5}\d{5,}$/,
									message: '잘못된 아이디 형식입니다.',
								},
							})}
							type='id'
							placeholder='id'
							onInput={clearFindError}
						/>
					</FormInput>
					{idError}
					<FormInput htmlFor='email'>
						<span>
							<VscMail />
						</span>
						<input
							{...register('email', {
								required: '이메일을 입력하세요',
								pattern: {
									value: /^\S+@\S+.\S+$/,
									message: '잘못된 이메일 형식입니다.',
								},
							})}
							type='email'
							placeholder='Email'
							onInput={clearFindError}
						/>
					</FormInput>
					{emailError}
					<FormBtn value='비밀번호 찾기' disabled={!isValid} />
				</form>
			</FormBox>
			<LinkBox>
				<ImEnter />
				<Link to={routes.login}>로그인</Link>
				<span>|</span>
				<Link to={routes.findid}>아이디 찾기</Link>
			</LinkBox>
		</AuthLayout>
	);
}

export default Findpw;
