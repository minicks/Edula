import _ from './_variables';

export type ThemeType = 'base' | 'dark' | 'nature' | 'twilight' | 'colorful';

const theme = {
	base: {
		fontColor: _.realBlack,
		bgColor: _.skyblue,
		subBgColor: _.white,
		warningColor: _.red,
		mainBlue: _.mainBlue,
		borderColor: _.lightGrey,
		iconColor: _.darkerWhite,
		iconColorActive: _.yellow,
		pointColor: _.pink,
	},
	dark: {
		fontColor: _.white,
		bgColor: _.realBlack,
		subBgColor: _.skyblue,
		warningColor: _.red,

		mainBlue: _.mainBlue,
		borderColor: _.lightGrey,
		iconColor: _.darkerWhite,
		iconColorActive: _.yellow,
		pointColor: _.pink,
	},
	nature: {
		fontColor: _.realBlack,
		bgColor: _.natureGreen,
		subBgColor: _.natureGreyBlue,
		warningColor: _.red,
		mainBlue: _.natureBrownGreen,
		borderColor: _.lightGrey,
		iconColor: _.darkerWhite,
		iconColorActive: _.natureGreen,
		pointColor: _.naturePink,
	},
	twilight: {
		fontColor: _.twilightBrown,
		bgColor: _.twilightPurple,
		subBgColor: _.twilightBlue,
		warningColor: _.red,
		mainBlue: _.twilightBlue,
		borderColor: _.lightGrey,
		iconColor: _.darkerWhite,
		iconColorActive: _.natureGreen,
		pointColor: _.twilightPink,
	},
	colorful: {
		fontColor: _.realBlack,
		bgColor: _.childrenyellow,
		subBgColor: _.childrenorange,
		warningColor: _.childrenred,
		mainBlue: _.childrengreen,
		borderColor: _.childrengreen,
		iconColor: _.darkerWhite,
		iconColorActive: _.childrengreen,
		pointColor: _.childrenyellow,
	},
};

export default theme;
