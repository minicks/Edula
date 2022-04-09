import { Fragment, useContext, useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import styled from 'styled-components';
import { MdCancel, MdModeEdit } from 'react-icons/md';
import {
	apiDeleteClassroomDetail,
	apiGetClassrooms,
} from '../../api/classroom';
import ClassroomForm from '../../components/admin/ClassroomForm';
import Table from '../../components/table/Table';
import Tbody from '../../components/table/Tbody';
import Tel from '../../components/table/Tel';
import UserContext from '../../context/user';
import routes from '../../routes';
import IconBtn from '../../common/IconBtn';
import Container from '../../components/admin/Container';
import TIContainer from '../../components/admin/TopInputContainer';
import TIWrapper from '../../components/admin/TopInputWrapper';
import TITitle from '../../components/admin/TopInputTitle';
import Btn from '../../common/Btn';
import PageTitle from '../../components/PageTitle';

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

function ClassManager() {
	const { schoolId } = useContext(UserContext);
	const [classrooms, setClassrooms] = useState([] as Classroom[]);
	const [editTarget, setEditTarget] = useState({} as Classroom);
	const [editMode, setEditMode] = useState(false);

	const getClassrooms = () => {
		apiGetClassrooms(schoolId).then(res => {
			setClassrooms(res.data);
		});
	};

	const deleteClassroom = async (classroomId: string) => {
		await apiDeleteClassroomDetail(schoolId, classroomId);
		getClassrooms();
	};

	useEffect(() => {
		if (schoolId) {
			getClassrooms();
		}
	}, [schoolId]);

	useEffect(() => {
		setEditMode(false);
		setEditTarget({} as Classroom);
	}, [classrooms]);

	return (
		<Container>
			<PageTitle title='학급 관리' />
			<TIContainer>
				<TIWrapper>
					<TITitle>학급 생성</TITitle>
					{!editMode && (
						<Btn
							onClick={() => {
								setEditMode(true);
								setEditTarget({} as Classroom);
							}}
						>
							생성
						</Btn>
					)}
					{editMode && !editTarget?.id && (
						<ClassroomForm
							targetClassroom={editTarget}
							getClassrooms={getClassrooms}
						/>
					)}
				</TIWrapper>
			</TIContainer>
			<Table>
				<Tbody>
					<Tel value='학년' />
					<Tel value='반' />
				</Tbody>
				{classrooms.map(e => (
					<Fragment key={e.id}>
						<Tbody>
							<Tel value={e.classGrade} />
							<SLink key={e.id} to={`${routes.classroom}/${e.id}`}>
								<Tel value={e.classNum} />
							</SLink>
							<IconBtn
								onClick={() => {
									setEditTarget(e);
									setEditMode(true);
								}}
							>
								<MdModeEdit />
							</IconBtn>
							<IconBtn onClick={() => deleteClassroom(e.id.toString())}>
								<MdCancel />
							</IconBtn>
						</Tbody>
						{editTarget === e && (
							<ClassroomForm targetClassroom={e} getClassrooms={getClassrooms} />
						)}
					</Fragment>
				))}
			</Table>
		</Container>
	);
}

export default ClassManager;
