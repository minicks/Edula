import { useContext, useEffect, useState } from 'react';
import { BiPhone } from 'react-icons/bi';
import { FiUser } from 'react-icons/fi';
import { VscMail } from 'react-icons/vsc';
import { FaUserEdit } from 'react-icons/fa';
import { useParams } from 'react-router-dom';
import styled from 'styled-components';
import {
	apiGetAdminInfo,
	apiGetStudentInfo,
	apiGetTeacherInfo,
	apiGetUserStatus,
} from '../api/user';
import UserContext from '../context/user';
import EditProfileForm from '../components/profile/EditProfileForm';
import EditPasswordForm from '../components/profile/EditPasswordForm';
import ScheduleContainer from '../components/schedule/ScheduleContainer';
import EditImgForm from '../components/profile/EditImgForm';
import PageTitle from '../components/PageTitle';

const UserContainer = styled.div`
	display: flex;
	margin: 50px;
`;

const UserInfoContainer = styled.div`
	display: flex;
	flex-direction: column;
	align-items: center;
`;

const UserProfileContainer = styled.div`
	height: 200px;
	width: 200px;
	background-color: white;
	border-radius: 50%;
	display: flex;
	justify-content: center;
	align-items: center;

	img {
		height: 100%;
		width: 100%;
		border-radius: 50%;
		background-size: cover;
	}
`;

const UserDataContainer = styled.div`
	& > div {
		margin-top: 15px;
		display: flex;
		align-items: center;
		padding: 5px;
	}

	svg {
		margin: 0 0.5rem;
	}

	.edit {
		background-color: inherit;
		border: 1px solid black;
		border-radius: 3px;
		margin-top: 20px;
		text-align: center;
		width: 100%;
		padding: 3px;

		&:hover {
			cursor: pointer;
			box-shadow: 0px 0px 3px black;
		}

		&:active {
			box-shadow: 0px 0px 5px black;
		}
	}

	.name {
		font-size: 3rem;
		font-weight: 600;
	}
`;

interface UserDataType {
	user: {
		id: number;
		firstName: string;
		status: string;
		username: string;
		email: string;
		phone: string;
		profileImage: string;
	};
	classroom: {
		id: number;
		classGrade: string;
		classNum: string;
	};
	school: {
		id: number;
		name: string;
	};
	guardianPhone?: string;
}

function Profile() {
	const { userId: loggedInUserId } = useContext(UserContext);
	const { userId } = useParams();
	const [userStat, setUserStat] = useState('');
	const [userData, setUserData] = useState({
		user: {},
		classroom: {},
		school: {},
		guardianPhone: '',
	} as UserDataType);
	const [editMode, setEditMode] = useState('profile');

	const toggleMode = (newMode: string) => {
		setEditMode(newMode);
	};

	const changeUserData = (newData: object) => {
		setUserData({
			...userData,
			...newData,
		});
		getUserData();
	};

	const getUserData = () => {
		switch (userStat) {
			case 'ST':
				apiGetStudentInfo(userId || '').then(res => {
					setUserData(res.data);
				});
				break;
			case 'TE':
				apiGetTeacherInfo(userId || '').then(res => {
					setUserData(res.data);
				});
				break;
			case 'SA':
				apiGetAdminInfo(userId || '').then(res => {
					setUserData(res.data);
				});
				break;
			default:
				break;
		}
	};

	useEffect(() => {
		apiGetUserStatus(userId || '').then(res => {
			setUserStat(res.data.status);
		});
	}, []);

	useEffect(() => {
		getUserData();
	}, [userStat]);

	const editBtn =
		loggedInUserId.toString() === userId ? (
			<button
				className='edit'
				type='button'
				onClick={() => toggleMode('editProfile')}
			>
				<FaUserEdit />
				정보 수정
			</button>
		) : null;

	const pwEditBtn =
		loggedInUserId.toString() === userId ? (
			<button
				className='edit'
				type='button'
				onClick={() => toggleMode('editPassword')}
			>
				<FaUserEdit />
				비밀번호 수정
			</button>
		) : null;

	const imgEditBtn =
		loggedInUserId.toString() === userId ? (
			<button className='edit' type='button' onClick={() => toggleMode('editImg')}>
				<FaUserEdit />
				프로필 사진 수정
			</button>
		) : null;

	const contents = (mode: string) => {
		switch (mode) {
			case 'editProfile':
				return (
					<EditProfileForm toggleMode={toggleMode} changeUserData={changeUserData} />
				);
			case 'editPassword':
				return <EditPasswordForm toggleMode={toggleMode} />;
			case 'editImg':
				return <EditImgForm toggleMode={toggleMode} />;
			default:
				return (
					<>
						<div className='name'>{userData?.user?.firstName}</div>
						<div className='class'>
							<FiUser />
							{userData?.school?.name}
							{userData?.classroom &&
								` ${userData?.classroom?.classGrade}학년 ${userData?.classroom?.classNum}반`}
						</div>
						<div className='email'>
							<VscMail />
							{userData?.user?.email}
						</div>
						<div className='phone'>
							<BiPhone />
							{userData?.user?.phone}
						</div>
						{userStat === 'ST' && (
							<div className='guadianPhone'>
								<BiPhone />
								{userData?.guardianPhone}
							</div>
						)}
						{editBtn}
						{pwEditBtn}
						{imgEditBtn}
					</>
				);
		}
	};

	return (
		<UserContainer>
			<PageTitle title={`${userData.user.firstName || '회원'}님의 프로필`} />
			<UserInfoContainer>
				<UserProfileContainer>
					<img
						src={
							userData.user.profileImage
								? `${process.env.REACT_APP_PROTOCOL}://${window.location.hostname}:${process.env.REACT_APP_PORT}${userData.user.profileImage}`
								: 'https://phinf.pstatic.net/contact/20201125_191/1606304847351yz0f4_JPEG/KakaoTalk_20201007_183735541.jpg?type=f130_130'
						}
						alt=''
					/>
				</UserProfileContainer>
				<UserDataContainer>{contents(editMode)}</UserDataContainer>
			</UserInfoContainer>
			<ScheduleContainer />
		</UserContainer>
	);
}

export default Profile;
