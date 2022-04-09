import { Fragment, useEffect, useState } from 'react';
import { MdCancel, MdModeEdit } from 'react-icons/md';
import { Link } from 'react-router-dom';
import styled from 'styled-components';
import { apiDeleteLectureDetail, apiGetLectures } from '../../api/lecture';
import Btn from '../../common/Btn';
import IconBtn from '../../common/IconBtn';
import Container from '../../components/admin/Container';
import LectureForm from '../../components/admin/LectureForm';
import TIContainer from '../../components/admin/TopInputContainer';
import TITitle from '../../components/admin/TopInputTitle';
import TIWrapper from '../../components/admin/TopInputWrapper';
import PageTitle from '../../components/PageTitle';
import Table from '../../components/table/Table';
import Tbody from '../../components/table/Tbody';
import Tel from '../../components/table/Tel';
import routes from '../../routes';

const SLink = styled(Link)`
	text-decoration: none;
	color: inherit;
`;

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

type LectureList = {
	day: string;
	st: string;
	end: string;
};

function LectureManager() {
	const [lectures, setLectures] = useState([] as Array<Lecture>);
	const [editTarget, setEditTarget] = useState({} as Lecture);
	const [editMode, setEditMode] = useState(false);

	const getLectures = () => {
		apiGetLectures().then(res => {
			setLectures(res.data);
		});
	};

	const deleteLecture = async (lectureId: string) => {
		await apiDeleteLectureDetail(lectureId);
		getLectures();
	};

	useEffect(() => {
		getLectures();
	}, []);

	useEffect(() => {
		setEditMode(false);
		setEditTarget({} as Lecture);
	}, [lectures]);

	return (
		<Container>
			<PageTitle title='수업 관리' />
			<TIContainer>
				<TIWrapper>
					<TITitle>수업 생성</TITitle>
					{!editMode && (
						<Btn
							onClick={() => {
								setEditMode(true);
								setEditTarget({} as Lecture);
							}}
						>
							생성
						</Btn>
					)}
					{editMode && !editTarget?.id && <LectureForm getLectures={getLectures} />}
				</TIWrapper>
			</TIContainer>
			<Table>
				<Tbody>
					<Tel value='이름' />
					<Tel value='담당 교사' />
					<Tel value='시간' />
				</Tbody>
				{lectures.map((e: Lecture) => (
					<Fragment key={e.id}>
						<Tbody>
							<SLink to={`/lecture/${e.id}`}>
								<Tel value={e.name} />
							</SLink>
							<SLink to={`${routes.profile}/${e.teacher?.id}`}>
								<Tel value={e.teacher?.firstName} />
							</SLink>
							<Tel value={e?.timeList.lectures.map(el => el.day).join(' ')} />
							<IconBtn
								onClick={() => {
									setEditTarget(e);
								}}
							>
								<MdModeEdit />
							</IconBtn>
							<IconBtn onClick={() => deleteLecture(e.id.toString())}>
								<MdCancel />
							</IconBtn>
						</Tbody>
						{editTarget === e && (
							<LectureForm targetLecture={e} getLectures={getLectures} />
						)}
					</Fragment>
				))}
			</Table>
		</Container>
	);
}

export default LectureManager;
