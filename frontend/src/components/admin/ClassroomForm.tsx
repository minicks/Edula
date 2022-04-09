import { AxiosError } from 'axios';
import { useContext } from 'react';
import { SubmitHandler, useForm } from 'react-hook-form';
import { apiPostClassroom, apiPutClassroomDetail } from '../../api/classroom';
import Btn from '../../common/Btn';
import UserContext from '../../context/user';
import FormBox from '../auth/FormBox';
import FormBtn from '../auth/FormBtn';
import FormInput from '../auth/FormInput';

interface Classroom {
	id: number;
	classGrade: number;
	classNum: number;
	school: number;
}

type ClassroomInput = {
	classGrade: number;
	classNum: number;
};

type PropType = {
	targetClassroom?: Classroom;
	getClassrooms: () => void;
};

function ClassroomForm({ targetClassroom, getClassrooms }: PropType) {
	const { schoolId } = useContext(UserContext);
	const {
		register,
		handleSubmit,
		formState: { errors, isValid },
		getValues,
		setError,
		clearErrors,
	} = useForm<ClassroomInput>({
		mode: 'onChange',
		defaultValues: {
			classGrade: targetClassroom?.classGrade,
			classNum: targetClassroom?.classNum,
		},
	});
	const onValidSubmit: SubmitHandler<ClassroomInput> = async () => {
		const classroom = getValues();
		try {
			if (!targetClassroom?.id) {
				await apiPostClassroom(schoolId, classroom);
			} else if (targetClassroom?.id) {
				await apiPutClassroomDetail(
					schoolId,
					targetClassroom.id.toString(),
					classroom
				);
			}
			getClassrooms();
		} catch (e) {
			const error = e as AxiosError;
			console.log(error.response);
		}
	};

	return (
		<FormBox>
			<form onSubmit={handleSubmit(onValidSubmit)}>
				<FormInput htmlFor='classGrade'>
					<input
						{...register('classGrade')}
						min='1'
						max='6'
						type='number'
						placeholder='학년'
					/>
				</FormInput>
				<FormInput htmlFor='classNum'>
					<input
						{...register('classNum')}
						min='1'
						max='99'
						type='number'
						placeholder='반'
					/>
				</FormInput>
				<FormBtn
					value={targetClassroom?.id ? '수정' : '생성'}
					disabled={!isValid}
				/>
				<Btn onClick={() => getClassrooms()}>취소</Btn>
			</form>
		</FormBox>
	);
}

export default ClassroomForm;
