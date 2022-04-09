import { useContext, useEffect } from 'react';
import { SubmitHandler, useForm } from 'react-hook-form';
import { useNavigate } from 'react-router-dom';
import UserContext from '../../context/user';
import routes from '../../routes';
import ErrorMsg from '../../components/auth/ErrorMsg';
import FormBox from '../../components/auth/FormBox';
import FormBtn from '../../components/auth/FormBtn';
import FormInput from '../../components/auth/FormInput';
import EmptyMsg from '../../components/auth/EmptyMsg';
import StyledTitle from '../../components/class/StyledTitle';
import StyledContent from '../../components/class/StyledContent';
import { apiSignup } from '../../api/schoolAdmin';
import AuthLayout from '../../components/auth/AuthLayout';
import PageTitle from '../../components/PageTitle';

type SignupInput = {
	result: string;
	firstName: string;
	password: string;
	passwordConfirmation: string;
	schoolAbbreviation: string;
	schoolName: string;
};
function Signup() {
	const { isLoggedIn } = useContext(UserContext);
	const {
		register,
		handleSubmit,
		formState: { errors, isValid },
		getValues,
		setError,
		clearErrors,
	} = useForm<SignupInput>({
		mode: 'onChange',
	});
	const navigate = useNavigate();

	useEffect(() => {
		if (isLoggedIn) {
			navigate(routes.main);
		}
	}, [isLoggedIn]);

	const clearSignupError = () => {
		clearErrors('result');
	};

	const resultError = errors.result?.message ? (
		<ErrorMsg message={errors.result?.message} />
	) : (
		<EmptyMsg />
	);

	const pwError = errors.password?.message ? (
		<ErrorMsg message={errors.password?.message} />
	) : (
		<EmptyMsg />
	);
	const pwConfirmationError = errors.passwordConfirmation?.message ? (
		<ErrorMsg message={errors.passwordConfirmation?.message} />
	) : (
		<EmptyMsg />
	);
	const schoolNameError = errors.schoolName?.message ? (
		<ErrorMsg message={errors.schoolName?.message} />
	) : (
		<EmptyMsg />
	);
	const schoolAbbError = errors.schoolAbbreviation?.message ? (
		<ErrorMsg message={errors.schoolAbbreviation?.message} />
	) : (
		<EmptyMsg />
	);
	const firstNameError = errors.firstName?.message ? (
		<ErrorMsg message={errors.firstName?.message} />
	) : (
		<EmptyMsg />
	);

	const onValidSubmit: SubmitHandler<SignupInput> = async () => {
		const {
			firstName,
			password,
			passwordConfirmation,
			schoolName,
			schoolAbbreviation,
		} = getValues();
		if (password !== passwordConfirmation) {
			setError('passwordConfirmation', {
				message: '비밀번호, 비밀번호 확인이 일치하지 않아요.',
			});
		} else {
			try {
				apiSignup(firstName, password, schoolName, schoolAbbreviation)
					.then(res => {
						if (res.data?.error) {
							const errorType = res.data?.error;
							if (errorType) {
								setError('result', {
									message: '학교 코드가 중복됩니다. 학교 코드를 변경해주세요.',
								});
							}
						} else {
							navigate(routes.login);
						}
					})
					.catch();
			} catch (e) {
				setError('result', { message: '정보를 잘못 입력했어요.' });
			}
		}
	};
	return (
		<AuthLayout>
			<PageTitle title='관리자 회원가입' />
			<StyledTitle> Edula 학교 관리자 회원가입</StyledTitle>
			<StyledContent>
				Edula 서비스를 사용하시려면, 학교 관리자만 회원 가입을 하면 됩니다 !
			</StyledContent>
			<StyledContent>
				교사와 학생 계정은 학교 관리자를 통해서 생성합니다.
			</StyledContent>

			<StyledContent>아이디는 학교 코드 + 00000입니다.</StyledContent>

			<FormBox>
				<form onSubmit={handleSubmit(onValidSubmit)}>
					{resultError}
					<FormInput htmlFor='schoolName'>
						<span>학교 이름</span>
						<input
							{...register('schoolName', {
								required: '학교 이름을 입력하세요.',
								minLength: {
									value: 1,
									message: '학교 이름은 최소 1글자, 최대 30글자입니다.',
								},
								maxLength: {
									value: 30,
									message: '학교 이름은 최소 1글자, 최대 30글자입니다.',
								},
							})}
							type='text'
							placeholder='학교 이름을 입력하세요.'
							onInput={clearSignupError}
						/>
					</FormInput>
					{schoolNameError}
					<FormInput htmlFor='schoolAbbreviation'>
						<span>학교 코드</span>
						<input
							{...register('schoolAbbreviation', {
								required: '학교 코드를 입력하세요.',
								minLength: {
									value: 3,
									message:
										'학교 코드는 영어 문자 3글자입니다. 대소문자 모두 가능하고, 대소문자를 구분합니다.',
								},
								maxLength: {
									value: 3,
									message:
										'학교 코드는 영어 문자 3글자입니다. 대소문자 모두 가능하고, 대소문자를 구분합니다.',
								},
								pattern: {
									value: /[a-zA-Z]{3}/,
									message:
										'학교 코드는 영어 문자 3글자입니다. 대소문자 모두 가능하고, 대소문자를 구분합니다.',
								},
							})}
							type='text'
							placeholder='학교 코드(영문자 3글자)를 입력하세요.'
							onInput={clearSignupError}
						/>
					</FormInput>
					{schoolAbbError}
					<FormInput htmlFor='firstName'>
						<span>계정 이름</span>
						<input
							{...register('firstName', {
								required: '관리자 계정 이름을 입력하세요.',
								minLength: {
									value: 1,
									message: '최소 1글자, 최대 30글자 가능합니다',
								},
								maxLength: {
									value: 30,
									message: '최소 1글자, 최대 30글자 가능합니다.',
								},
							})}
							type='text'
							placeholder='관리자 계정 이름을 입력하세요.'
							onInput={clearSignupError}
						/>
					</FormInput>
					{firstNameError}
					<FormInput htmlFor='password'>
						<div>비밀번호</div>
						<input
							{...register('password', {
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
							placeholder='비밀 번호를 입력하세요. (8~16자)'
							onInput={clearSignupError}
						/>
					</FormInput>
					{pwError}
					<FormInput htmlFor='passwordConfirmation'>
						<div>비밀번호 확인</div>
						<input
							{...register('passwordConfirmation', {
								required: 'passwordConfirmation.',
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
							placeholder='비밀 번호를 다시 한번 입력하세요.'
							onInput={clearSignupError}
						/>
					</FormInput>
					{pwConfirmationError}
					<FormBtn value='회원 가입' disabled={!isValid} />
				</form>
			</FormBox>
		</AuthLayout>
	);
}

export default Signup;
