import { useContext } from 'react';
import { SubmitHandler, useForm } from 'react-hook-form';
import {
	apiGetClassroomDetail,
	apiGetClassrooms,
	apiPutClassroomDetail,
} from '../../api/classroom';
import { apiPutUser } from '../../api/schoolAdmin';
import { apiPutStudentInfo } from '../../api/user';
import UserContext from '../../context/user';
import FormBox from '../auth/FormBox';
import FormBtn from '../auth/FormBtn';
import FormInput from '../auth/FormInput';
import StudentList from '../class/StudentList';

interface Classroom {
	id: number;
	classGrade: number;
	classNum: number;
	school: number;
}

interface School {
	id: number;
	name: string;
	abbreviation: string;
}

interface User {
	id: number;
	username?: string;
	firstName?: string;
	status?: string;
	email?: string;
	phone?: string;
}

interface Student {
	classroom?: Classroom;
	guardianPhone?: string;
	school?: School;
	user: User;
}

type StudentInput = {
	classGrade: number;
	classNum: number;
	name: string;
	email: string;
	phone: string;
	guardianPhone: string;
};

type PropType = {
	targetUser: Student;
	getUsers: () => void;
};

function UserForm({ targetUser, getUsers }: PropType) {
	const { schoolId } = useContext(UserContext);
	const {
		register,
		handleSubmit,
		formState: { errors, isValid },
		getValues,
		setError,
		clearErrors,
	} = useForm<StudentInput>({
		mode: 'onChange',
		defaultValues: {
			classGrade: targetUser?.classroom?.classGrade,
			classNum: targetUser?.classroom?.classNum,
			name: targetUser?.user?.firstName,
			email: targetUser?.user?.email,
			phone: targetUser?.user?.phone,
			guardianPhone: targetUser?.guardianPhone,
		},
	});

	const onValidSubmit: SubmitHandler<StudentInput> = async () => {
		const { classGrade, classNum, name, email, phone, guardianPhone } =
			getValues();
		try {
			await apiPutUser(targetUser.user.id, { firstName: name, email, phone });
			if (targetUser.user.status === 'ST') {
				await apiPutStudentInfo(
					targetUser.user.id.toString(),
					{ email, phone },
					guardianPhone
				);
			}
			await apiGetClassrooms(schoolId).then(async res => {
				const matchedClassroom = res.data.filter(
					// eslint-disable-next-line eqeqeq
					(e: Classroom) => e.classGrade == classGrade && e.classNum == classNum
				);
				if (matchedClassroom.length === 1) {
					let teacher: number = 0;
					let studentList = [] as Array<number>;
					await apiGetClassroomDetail(schoolId, matchedClassroom[0].id).then(
						response => {
							teacher = response.data.teacher;
							studentList = response.data.studentList.map((e: Student) => e.user.id);
						}
					);
					if (targetUser.user.status === 'ST') {
						studentList.push(targetUser.user.id);
					} else if (targetUser.user.status === 'TE') {
						teacher = targetUser.user.id;
					}
					console.log(teacher, studentList);
					const classroom = {
						classGrade,
						classNum,
						teacher,
						studentList,
					};
					console.log(matchedClassroom[0], classroom);
					await apiPutClassroomDetail(
						schoolId,
						matchedClassroom[0].id.toString(),
						classroom
					).then(res => console.log(res));
				}
			});
		} catch (e) {
			// const error = e as AxiosError;
			// if (error?.response?.status === 401) {
			// 	navigate(routes.login);
			// }
		}
		getUsers();
	};

	return (
		<FormBox>
			<form onSubmit={handleSubmit(onValidSubmit)}>
				<FormInput htmlFor='classGrade'>
					<input {...register('classGrade')} placeholder='학년' />
				</FormInput>
				<FormInput htmlFor='classNum'>
					<input {...register('classNum')} placeholder='반' />
				</FormInput>
				<FormInput htmlFor='name'>
					<input {...register('name')} placeholder='이름' />
				</FormInput>
				<FormInput htmlFor='email'>
					<input {...register('email')} placeholder='이메일' />
				</FormInput>
				<FormInput htmlFor='phone'>
					<input {...register('phone')} placeholder='전화번호' />
				</FormInput>
				{targetUser?.user?.status === 'ST' && (
					<FormInput htmlFor='guardianPhone'>
						<input {...register('guardianPhone')} placeholder='보호자 전화번호' />
					</FormInput>
				)}
				<FormBtn value='수정' disabled={!isValid} />
			</form>
		</FormBox>
	);
}

export default UserForm;
