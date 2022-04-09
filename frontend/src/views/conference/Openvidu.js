import { OpenVidu } from 'openvidu-browser';
import { useState, useEffect, useContext } from 'react';
import { AiOutlineAudio, AiOutlineAudioMuted } from 'react-icons/ai';
import { FiVideo, FiVideoOff } from 'react-icons/fi';
import { ImExit } from 'react-icons/im';
import {
	MdCameraswitch,
	MdOutlineScreenShare,
	MdOutlineStopScreenShare,
	MdSend,
} from 'react-icons/md';
import styled from 'styled-components';
import { createSession, createToken } from '../../api/conference';
import AuthLayout from '../../components/auth/AuthLayout';
import FormInput from '../../components/auth/FormInput';
import UserVideoComponent from '../../components/conference/UserVideoComponent';
import PageTitle from '../../components/PageTitle';
import UserContext from '../../context/user';

const Container = styled.div`
	width: 100vw;
	height: 100vh;
	box-sizing: border-box;
`;

const ConferenceContainer = styled.div`
	display: grid;
	grid-template-columns: repeat(9, 1fr);
	grid-auto-rows: minmax(3em, auto);
	grid-template-areas:
		'top top top top top top top top top'
		'sd sd main main main main main main main';
`;

const TopBar = styled.div`
	grid-area: top;
	width: 100%;
	display: flex;
	justify-content: center;
	align-items: center;
`;

const SideBar = styled.div`
	grid-area: sd;
	height: calc(100vh - 4em);
	display: grid;
	grid-template-rows: 3fr 7fr;
	margin-left: 5px;
`;

const MemberContainer = styled.div`
	height: 100%;
	padding: 0.25em;
	margin: 0.25em;
	box-sizing: border-box;
	background-color: ${props => props.theme.subBgColor};
	border-radius: 3px;
	border: 1px solid ${props => props.theme.borderColor};
	overflow: hidden;
	& > p {
		padding: 0.5em;
		font-size: 1.2em;
	}
`;

const MemberContents = styled.div`
	background-color: ${props => props.theme.subBgColor};
	border: 1px solid ${props => props.theme.borderColor};
	display: flex;
	flex-direction: column;
	width: 100%;
	height: 100%;
	border-radius: 3px;
	padding: 0.5em;
	box-sizing: border-box;
	overflow-y: scroll;

	p {
		margin: 0.1em;
	}
`;

const ChatContainer = styled.div`
	height: 100%;
	padding: 0.25em;
	margin: 0.25em;
	box-sizing: border-box;
	background-color: ${props => props.theme.subBgColor};
	border: 1px solid ${props => props.theme.borderColor};
	border-radius: 3px;
	overflow: hidden;
`;

const ChatContents = styled.div`
	min-height: calc(100% - 3em);
	max-height: calc(100% - 3em);
	background-color: ${props => props.theme.subBgColor};
	border: 1px solid ${props => props.theme.borderColor};
	display: flex;
	flex-direction: column-reverse;
	overflow-y: scroll;
	border-radius: 3px;

	& > div {
		display: flex;
		flex-direction: column;
		justify-content: end;
		padding: 0.6em;

		& > div {
			margin: 0.2em;
			font-size: 1.2em;
			overflow-wrap: break-word;
		}
	}
`;

const ChatInputContainer = styled.div`
	height: 3em;
	background-color: ${props => props.theme.subBgColor};
	border: 1px solid ${props => props.theme.borderColor};
	display: flex;
	justify-content: center;
	align-items: center;
	border-radius: 3px;
	form {
		display: flex;
		justify-content: center;
		align-items: center;

		input,
		button {
			border-radius: 3px;
			padding: 0.2em;
		}

		button {
			background-color: inherit;
		}
	}
`;

const Main = styled.div`
	grid-area: main;
	width: 100%;
	height: 100%;
`;

const SessionContainer = styled.div`
	display: flex;
	justify-content: center;
	align-items: center;
	flex-wrap: wrap;
	width: 100%;
	height: 90%;
	overflow-y: scroll;
`;

const ScreenContainer = styled.div`
	video {
		width: 95%;
		height: 95%;
		object-fit: cover;
	}
`;

const VideoContainer = styled.div`
	width: 300px;
	height: 200px;
	text-align: center;
	button {
		width: 300px;
		height: 200px;
		border: 0;
		padding: 0;
		background-color: inherit;
	}
	button > video,
	video {
		width: 95%;
		height: 95%;
		object-fit: cover;
	}
`;

const BottomFns = styled.div`
	position: absolute;
	bottom: 2em;
	left: 40%;
	display: flex;
	justify-content: center;
	align-items: center;
	background-color: ${props => props.theme.subBgColor};
	padding: 0.5em;
	border-radius: 1em;

	button {
		border-radius: 50%;
		padding: 0.25em;
		font-size: 2em;
		margin: 0 0.5em;
	}

	#buttonLeaveSession {
		color: ${props => props.theme.warningColor};
	}
`;

const SButton = styled.button`
	display: flex;
	justify-content: center;
	align-items: center;
	background-color: inherit;
`;

function Openvidu() {
	const { currentLecture: mySessionId, userName: myUserName } =
		useContext(UserContext);
	// const [mySessionId, setMySessionId] = useState('SessionA');
	// const [myUserName, setMyUserName] = useState(
	// 	`Participant${Math.floor(Math.random() * 100)}`
	// );
	const [sessionCamera, setSessionCamera] = useState(undefined);
	const [sessionScreen, setSessionScreen] = useState(undefined);
	const [sessionChat, setSessionChat] = useState(undefined);
	const [mainStreamManager, setMainStreamManager] = useState(undefined);
	const [publisher, setPublisher] = useState(undefined);
	const [publisherScreen, setPublisherScreen] = useState(undefined);
	const [subscribers, setSubscribers] = useState([]);
	const [currentVideoDevice, setCurrentVideoDevice] = useState(undefined);
	const [OVCamera, setOVCamera] = useState(null);
	const [OVScreen, setOVScreen] = useState(null);
	const [OVChat, setOVChat] = useState(null);
	const [screensharing, setScreensharing] = useState(null);
	const [audioEnabled, setAudioEnabled] = useState(true);
	const [videoEnabled, setVideoEnabled] = useState(true);
	const [myMessage, setMyMessage] = useState('');
	const [messages, setMessages] = useState([]);

	useEffect(() => {
		window.addEventListener('beforeunload', onbeforeunload);
		window.addEventListener('popstate', onBackButtonEvent);
		return () => {
			window.removeEventListener('beforeunload', onbeforeunload);
			window.removeEventListener('popstate', onBackButtonEvent);
		};
	});

	const handleChangeMyMessage = e => {
		setMyMessage(e.target.value);
	};

	const handleMainVideoStream = stream => {
		if (mainStreamManager !== stream) {
			setMainStreamManager(stream);
		}
	};

	const onBackButtonEvent = e => {
		e.preventDefault();
		leaveSession();
	};

	const onbeforeunload = () => {
		leaveSession();
	};

	const getToken = async () => {
		const sessionId = await createSession(mySessionId);
		const tokenTmp = await createToken(sessionId);
		return tokenTmp;
	};

	const joinSession = () => {
		console.log(`mySessionId : ${mySessionId}`);
		console.log(`myUserName : ${myUserName}`);
		const OVCameraTmp = new OpenVidu();
		const OVScreenTmp = new OpenVidu();
		const OVChatTmp = new OpenVidu();
		setOVCamera(OVCameraTmp);
		setOVScreen(OVScreenTmp);
		setOVChat(OVChatTmp);
		setSessionCamera(OVCameraTmp.initSession());
		setSessionScreen(OVScreenTmp.initSession());
		setSessionChat(OVChatTmp.initSession());
	};

	const sendMessage = e => {
		e.preventDefault();
		setMyMessage(preMyMessage => {
			(async () => {
				try {
					await sessionChat.signal({
						data: `${preMyMessage}`, // Any string (optional)
						to: [], // Array of Connection objects (optional. Broadcast to everyone if empty)
						// type: 'my-chat', // The type of message (optional)
					});
					console.log('Message successfully sent');
				} catch (error) {
					console.error(error);
				}
			})();
			return '';
		});
	};

	useEffect(async () => {
		if (!sessionCamera) {
			return;
		}

		sessionCamera.on('streamCreated', event => {
			if (event.stream.typeOfVideo === 'CAMERA') {
				const subscriber = sessionCamera.subscribe(event.stream, undefined);
				setSubscribers(prevSubscribers => prevSubscribers.concat([subscriber]));
			}
		});

		sessionCamera.on('streamDestroyed', event => {
			deleteSubscriber(event.stream.streamManager);
		});

		sessionCamera.on('exception', exception => {
			console.warn(exception);
		});

		try {
			const token = await getToken();
			await sessionCamera.connect(token, { clientData: myUserName });
			const devices = await OVCamera.getDevices();
			const videoDevices = devices.filter(device => device.kind === 'videoinput');

			const newPublisher = OVCamera.initPublisher(undefined, {
				audioSource: undefined, // The source of audio. If undefined default microphone
				videoSource: videoDevices[0].deviceId, // The source of video. If undefined default webcam
				publishAudio: true, // Whether you want to start publishing with your audio unmuted or not
				publishVideo: true, // Whether you want to start publishing with your video enabled or not
				resolution: '640x480', // The resolution of your video
				frameRate: 30, // The frame rate of your video
				insertMode: 'APPEND', // How the video is inserted in the target element 'video-container'
				mirror: false, // Whether to mirror your local video or not
			});

			sessionCamera.publish(newPublisher);

			setCurrentVideoDevice(videoDevices[0]);
			setMainStreamManager(newPublisher);
			setPublisher(newPublisher);
		} catch (error) {
			console.log(
				'There was an error connecting to the sessionCamera:',
				error.code,
				error.message
			);
		}
	}, [sessionCamera]);

	useEffect(async () => {
		if (!sessionScreen) {
			return;
		}

		sessionScreen.on('streamCreated', event => {
			if (event.stream.typeOfVideo === 'SCREEN') {
				sessionScreen.subscribe(event.stream, 'container-screens');
				// When the HTML video has been appended to DOM...
				// subscriberScreen.on('videoElementCreated', event => {
				// 	// Add a new <p> element for the user's nickname just below its video
				// 	// appendUserData(event.element, subscriberScreen.stream.connection);
				// });
			}
		});

		try {
			const token = await getToken();
			await sessionScreen.connect(token, { clientData: myUserName });
			console.log('Session screen connected');
		} catch (error) {
			console.warn(
				'There was an error connecting to the session for screen share:',
				error.code,
				error.message
			);
		}
	}, [sessionScreen]);

	useEffect(async () => {
		if (!sessionChat) {
			return;
		}

		// Receiver of the message (usually before calling 'session.connect')
		// sessionChat.on('signal:my-chat', event => {
		// 	console.log(event.data); // Message
		// 	console.log(event.from); // Connection object of the sender
		// 	console.log(event.type); // The type of message ("my-chat")
		// });

		// Receiver of all messages (usually before calling 'session.connect')
		sessionChat.on('signal', event => {
			setMessages(preMessages => {
				console.log(event.data); // Message
				console.log(event.from); // Connection object of the sender
				console.log(event.type); // The type of message
				const id = event.from.creationTime;
				const msg = event.data;
				const user = JSON.parse(event.from.data);
				return preMessages.concat([{ id, msg, user: user.clientData }]);
			});
		});

		sessionChat.on('connectionCreated', event => {
			console.log(event.connection);
		});

		try {
			const token = await getToken();
			await sessionChat.connect(token, { clientData: myUserName });
			console.log('Session chat connected');
		} catch (error) {
			console.warn(
				'There was an error connecting to the session for chat:',
				error.code,
				error.message
			);
		}
	}, [sessionChat]);

	const publishScreenShare = () => {
		const newPublisherScreen = OVScreen.initPublisher('container-screens', {
			videoSource: 'screen',
		});

		newPublisherScreen.once('accessAllowed', event => {
			setScreensharing(true);
			newPublisherScreen.stream
				.getMediaStream()
				.getVideoTracks()[0]
				.addEventListener('ended', () => {
					console.log('User pressed the "Stop sharing" button');
					sessionScreen.unpublish(newPublisherScreen);
					setScreensharing(false);
				});
			sessionScreen.publish(newPublisherScreen);
		});

		// publisherScreen.on('videoElementCreated', event => {
		// 	// appendUserData(event.element, sessionScreen.connection);
		// 	// event.element['muted'] = true;
		// });

		newPublisherScreen.once('accessDenied', event => {
			console.error('Screen Share: Access Denied');
		});

		setPublisherScreen(newPublisherScreen);
	};

	const stopScreenShare = () => {
		console.log('User pressed the "Stop sharing" button');
		sessionScreen.unpublish(publisherScreen);
		setScreensharing(false);
	};

	const leaveSession = () => {
		if (sessionCamera) {
			sessionCamera.disconnect();
		}

		if (sessionScreen) {
			sessionScreen.disconnect();
		}

		if (sessionChat) {
			sessionChat.disconnect();
		}

		setOVCamera(null);
		setOVScreen(null);
		setOVChat(null);
		setSessionCamera(undefined);
		setSessionScreen(undefined);
		setSessionChat(undefined);
		setSubscribers([]);
		setMessages([]);
		// setMySessionId('SessionA');
		// setMyUserName(`Participant${Math.floor(Math.random() * 100)}`);
		setMainStreamManager(undefined);
		setPublisher(undefined);
		setPublisherScreen(undefined);
	};

	const switchCamera = async () => {
		try {
			const devices = await OVCamera.getDevices();
			const videoDevices = devices.filter(device => device.kind === 'videoinput');

			if (videoDevices && videoDevices.length > 1) {
				const newVideoDevice = videoDevices.filter(
					device => device.deviceId !== currentVideoDevice.deviceId
				);

				if (newVideoDevice.length > 0) {
					const newPublisher = OVCamera.initPublisher(undefined, {
						videoSource: newVideoDevice[0].deviceId,
						publishAudio: true,
						publishVideo: true,
						mirror: true,
					});

					await sessionCamera.unpublish(mainStreamManager);
					await sessionCamera.publish(newPublisher);
					setCurrentVideoDevice(newVideoDevice);
					setMainStreamManager(newPublisher);
					setPublisher(newPublisher);
				}
			}
		} catch (e) {
			console.error(e);
		}
	};

	const audioOnOFF = () => {
		setAudioEnabled(preAudioEnabled => {
			publisher.publishAudio(!preAudioEnabled);
			return !preAudioEnabled;
		});
	};

	const videoOnOFF = () => {
		setVideoEnabled(preVideoEnabled => {
			publisher.publishVideo(!preVideoEnabled);
			return !preVideoEnabled;
		});
	};

	const deleteSubscriber = streamManager => {
		setSubscribers(prevSubscribers => {
			const tmpSubscribers = Array.from(prevSubscribers);
			const index = tmpSubscribers.indexOf(streamManager, 0);
			if (index > -1) {
				tmpSubscribers.splice(index, 1);
			}
			return tmpSubscribers;
		});
	};

	return (
		<Container>
			<PageTitle title={`${mySessionId} 교실`} />
			{!sessionCamera && (
				<AuthLayout>
					<h1> 수업 참여 </h1>
					<SButton type='button' onClick={() => joinSession()}>
						참여하기
					</SButton>
				</AuthLayout>
			)}
			{sessionCamera && (
				<ConferenceContainer>
					<TopBar>
						<h1 id='session-title'>{mySessionId}</h1>
					</TopBar>
					<SideBar>
						<MemberContainer>
							<p>참여자 목록</p>
							<MemberContents>
								<div>
									{publisher && (
										<p>{JSON.parse(publisher.stream.connection.data).clientData}</p>
									)}
									{subscribers &&
										subscribers.map(sub => (
											<p key={sub}>{JSON.parse(sub.stream.connection.data).clientData}</p>
										))}
								</div>
							</MemberContents>
						</MemberContainer>
						<ChatContainer>
							<ChatContents>
								<div>
									{messages.slice().map(data => (
										<div key={data.id}>{`${data.user} : ${data.msg}`}</div>
									))}
								</div>
							</ChatContents>
							<ChatInputContainer>
								<form onSubmit={sendMessage}>
									<FormInput>
										<input
											type='text'
											id='message'
											placeholder='Message'
											value={myMessage}
											onChange={handleChangeMyMessage}
											required
										/>
									</FormInput>
									<button type='submit' name='commit'>
										<MdSend />
									</button>
								</form>
							</ChatInputContainer>
						</ChatContainer>
					</SideBar>
					<Main>
						<SessionContainer videoCount={subscribers.length}>
							<ScreenContainer id='container-screens' />
							<>
								{publisher && (
									<VideoContainer className='publisher'>
										<button
											onClick={() => handleMainVideoStream(publisher)}
											type='button'
										>
											<UserVideoComponent streamManager={publisher} />
										</button>
									</VideoContainer>
								)}
								{subscribers.map(sub => (
									<VideoContainer className='subscriber'>
										<button
											key={sub}
											onClick={() => handleMainVideoStream(sub)}
											type='button'
										>
											<UserVideoComponent streamManager={sub} />
										</button>
									</VideoContainer>
								))}
							</>
						</SessionContainer>
						<BottomFns>
							<SButton type='button' id='buttonSwitchCamera' onClick={switchCamera}>
								<MdCameraswitch />
							</SButton>
							{!screensharing ? (
								<SButton
									type='button'
									id='buttonScreenShare'
									onClick={publishScreenShare}
								>
									<MdOutlineScreenShare />
								</SButton>
							) : (
								<SButton type='button' id='buttonScreenShare' onClick={stopScreenShare}>
									<MdOutlineStopScreenShare />
								</SButton>
							)}
							<SButton type='button' id='buttonAudioOnOff' onClick={audioOnOFF}>
								{!audioEnabled ? <AiOutlineAudioMuted /> : <AiOutlineAudio />}
							</SButton>
							<SButton type='button' id='buttonVideoOnOff' onClick={videoOnOFF}>
								{!videoEnabled ? <FiVideoOff /> : <FiVideo />}
							</SButton>
							<SButton type='button' id='buttonLeaveSession' onClick={leaveSession}>
								<ImExit />
							</SButton>
						</BottomFns>
					</Main>
				</ConferenceContainer>
			)}
		</Container>
	);
}

export default Openvidu;
