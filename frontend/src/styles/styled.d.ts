import 'styled-components';

declare module 'styled-components' {
	export interface DefaultTheme {
		fontColor: string;
		bgColor: string;
		subBgColor: string;
		warningColor: string;
		mainBlue: string;
		borderColor: string;
		iconColor: string;
		iconColorActive: string;
		pointColor: string;
	}
}
