import { useContext, useEffect, useState } from 'react';
import { SubmitHandler, useForm } from 'react-hook-form';
import { MdCancel } from 'react-icons/md';
import styled from 'styled-components';
import { apiPostLecture, apiPutLectureDetail } from '../../api/lecture';
import Btn from '../../common/Btn';
import IconBtn from '../../common/IconBtn';
import UserContext from '../../context/user';
import FormBox from '../auth/FormBox';
import FormBtn from '../auth/FormBtn';
import FormInput from '../auth/FormInput';

const ListContainer = styled.div`
	display: flex;

	& > div {
		display: flex;
		justify-content: center;
		align-items: center;
		margin-right: 3px;
	}
`;

type LectureList = {
	day: string;
	st: string;
	end: string;
};

interface User {
	firstName: string;
	id: number;
	status: string;
	username: string;
}

interface Lecture {
	id: number;
	name: string;
	school: number;
	studentList: Array<number>;
	teacher: User;
	timeList: TimeList;
}

type TimeList = {
	count: number;
	lectures: Array<LectureList>;
};

type LectureInput = {
	name: string;
	timeList?: Array<TimeList>;
	teacher: number;
	studentList?: Array<number>;
};

type PropType = {
	targetLecture?: Lecture;
	getLectures: () => void;
};

function LectureForm({ targetLecture, getLectures }: PropType) {
	const { schoolId } = useContext(UserContext);
	const [timeList, setTimeList] = useState({
		count: targetLecture?.timeList?.count || 0,
		lectures: targetLecture?.timeList?.lectures || [],
	} as TimeList);
	const [studentList, setStudentList] = useState(
		targetLecture?.studentList || ([] as Array<number>)
	);
	const {
		register,
		handleSubmit,
		formState: { errors, isValid },
		getValues,
		setError,
		clearErrors,
	} = useForm<LectureInput>({
		mode: 'onChange',
		defaultValues: {
			name: targetLecture?.name,
			teacher: targetLecture?.teacher?.id,
		},
	});

	const onValidSubmit: SubmitHandler<LectureInput> = async () => {
		const { name, teacher } = getValues();

		const lecture = {
			name,
			teacher,
			school: schoolId,
			timeList,
			studentList,
		};
		try {
			if (!targetLecture?.id) {
				await apiPostLecture(lecture);
			} else if (targetLecture?.id) {
				await apiPutLectureDetail(targetLecture.id.toString(), lecture);
			}
			getLectures();
		} catch (e) {
			//
		}
	};

	const addTime = () => {
		const day = (document.getElementById('day') as HTMLInputElement).value;
		const st = (document.getElementById('start') as HTMLInputElement).value;
		const end = (document.getElementById('end') as HTMLInputElement).value;

		const newTime: LectureList = {
			day,
			st,
			end,
		};

		const newTimeList: TimeList = {
			count: timeList.lectures.length + 1,
			lectures: [...timeList.lectures, newTime],
		};

		setTimeList(newTimeList as TimeList);
	};

	const removeTime = (idx: number) => {
		const newTimeList: TimeList = {
			count: timeList.lectures.length - 1,
			lectures: timeList.lectures.filter((_, i) => i !== idx),
		};
		setTimeList(newTimeList);
	};

	const addStudent = () => {
		const newStudent = parseInt(
			(document.getElementById('student') as HTMLInputElement).value,
			10
		);
		if (studentList.indexOf(newStudent) === -1) {
			setStudentList(studentList.concat([newStudent]));
		}
	};

	const removeStudent = (idx: number) => {
		setStudentList(studentList.filter((_, i) => i !== idx));
	};

	return (
		<FormBox>
			<form onSubmit={handleSubmit(onValidSubmit)}>
				<FormInput htmlFor='name'>
					<input {...register('name')} placeholder='?????? ??????' />
				</FormInput>
				<FormInput htmlFor='teacher'>
					<input {...register('teacher')} placeholder='?????? pk' />
				</FormInput>
				<ListContainer>
					{timeList?.lectures?.map((e, idx) => (
						<div key={e.day + e.st + e.end}>
							<span>{e.day}</span>
							<span>{e.st}</span>
							<span>{e.end}</span>
							<IconBtn onClick={() => removeTime(idx)}>
								<MdCancel />
							</IconBtn>
						</div>
					))}
				</ListContainer>
				<div>
					?????????
					<input type='text' id='day' placeholder='??????' />
					<input type='text' id='start' placeholder='?????? ??????' />
					<input type='text' id='end' placeholder='?????? ??????' />
					<button type='button' onClick={() => addTime()}>
						??????
					</button>
				</div>
				<ListContainer>
					{studentList.map((e, idx) => (
						<div id={`${e}`} key={e}>
							<span>{e}</span>
							<IconBtn onClick={() => removeStudent(idx)}>
								<MdCancel />
							</IconBtn>
						</div>
					))}
				</ListContainer>
				<div>
					??????
					<input type='text' id='student' placeholder='?????? PK' />
					<button type='button' onClick={() => addStudent()}>
						??????
					</button>
				</div>
				<FormBtn value={targetLecture?.id ? '??????' : '??????'} disabled={!isValid} />
				<Btn onClick={() => getLectures()}>??????</Btn>
			</form>
		</FormBox>
	);
}

export default LectureForm;
