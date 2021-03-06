import { Fragment, useContext, useEffect, useState } from 'react';
import { MdCancel, MdModeEdit } from 'react-icons/md';
import { Link } from 'react-router-dom';
import styled from 'styled-components';
import { apiGetStudents } from '../../api/school';
import {
	apiCreateUsers,
	apiDeleteUser,
	apiDeleteUsers,
} from '../../api/schoolAdmin';
import Btn from '../../common/Btn';
import IconBtn from '../../common/IconBtn';
import Container from '../../components/admin/Container';
import TIContainer from '../../components/admin/TopInputContainer';
import TITitle from '../../components/admin/TopInputTitle';
import TIWrapper from '../../components/admin/TopInputWrapper';
import UserForm from '../../components/admin/UserForm';
import FormInput from '../../components/auth/FormInput';
import PageTitle from '../../components/PageTitle';
import MediumTel from '../../components/table/MTel';
import SmallTel from '../../components/table/STel';
import Table from '../../components/table/Table';
import Tbody from '../../components/table/Tbody';
import Tel from '../../components/table/Tel';
import UserContext from '../../context/user';
import routes from '../../routes';

const SLink = styled(Link)`
	text-decoration: none;
	color: inherit;
`;

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

function StudentManager() {
	const { schoolId } = useContext(UserContext);
	const [students, setStudents] = useState([] as Student[]);
	const [editTarget, setEditTarget] = useState({} as Student);
	const [editMode, setEditMode] = useState(false);

	const getStudents = () => {
		apiGetStudents(schoolId).then(res => {
			setStudents(res.data);
		});
	};

	const deleteStudent = async (studentId: string) => {
		await apiDeleteUser(studentId);
		getStudents();
	};

	const deleteStudents = async () => {
		const year = document.getElementById('deleteYear') as HTMLInputElement;
		await apiDeleteUsers(year.value);
		getStudents();
	};

	const createStudents = async () => {
		const year = document.getElementById('createYear') as HTMLInputElement;
		const count = document.getElementById('count') as HTMLInputElement;
		const studentCreationCountList = {} as any;
		studentCreationCountList[year.value] = parseInt(count.value, 10);

		await apiCreateUsers({
			studentCreationCountList,
			teacherCreationCount: 0,
		});
		getStudents();
	};

	useEffect(() => {
		if (schoolId) {
			getStudents();
		}
	}, [schoolId]);

	useEffect(() => {
		setEditMode(false);
		setEditTarget({} as Student);
	}, [students]);

	return (
		<Container>
			<PageTitle title='?????? ??????' />
			<TIContainer>
				<TIWrapper>
					<TITitle>?????? ??????</TITitle>
					<FormInput>
						<input type='text' id='createYear' placeholder='????????????' />
						<input type='text' id='count' placeholder='?????? ???' />
					</FormInput>
					<Btn onClick={() => createStudents()}>??????</Btn>
				</TIWrapper>
				<TIWrapper>
					<TITitle>?????? ??????</TITitle>
					<FormInput>
						<input type='text' id='deleteYear' placeholder='????????????' />
					</FormInput>
					<Btn onClick={() => deleteStudents()}>??????</Btn>
				</TIWrapper>
			</TIContainer>
			<Table>
				<Tbody>
					<SmallTel value='??????' />
					<SmallTel value='???' />
					<MediumTel value='?????????' />
					<MediumTel value='??????' />
					<Tel value='?????????' />
					<Tel value='????????????' />
					<Tel value='???????????????' />
				</Tbody>
				{students.map(e => (
					<Fragment key={e.user.id}>
						<Tbody>
							<SmallTel value={`${e?.classroom?.classGrade || '-'}`} />
							<SmallTel value={`${e?.classroom?.classNum || '-'}`} />
							<MediumTel value={e.user?.username || '-'} />
							<SLink to={`${routes.profile}/${e.user.id}`}>
								<MediumTel value={e.user?.firstName || '-'} />
							</SLink>
							<Tel value={e.user?.email || '-'} />
							<Tel value={e.user?.phone || '-'} />
							<Tel value={e?.guardianPhone || '-'} />
							<IconBtn
								onClick={() => {
									setEditTarget(e);
									setEditMode(true);
								}}
							>
								<MdModeEdit />
							</IconBtn>
							<IconBtn onClick={() => deleteStudent(e.user.id.toString())}>
								<MdCancel />
							</IconBtn>
						</Tbody>
						{editTarget === e && editMode && (
							<UserForm targetUser={e} getUsers={getStudents} />
						)}
					</Fragment>
				))}
			</Table>
		</Container>
	);
}

export default StudentManager;
