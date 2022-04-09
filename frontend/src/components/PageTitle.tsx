import { Helmet } from 'react-helmet';

type PropType = {
	title: string;
};

function PageTitle({ title }: PropType) {
	return (
		<Helmet>
			<title>{title} | Edula ~</title>
		</Helmet>
	);
}

export default PageTitle;
