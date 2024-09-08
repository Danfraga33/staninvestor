import { useEffect, useState } from 'react';
import './App.css';

function App() {
	const [data, setData] = useState();
	useEffect(() => {
		const fetchData = async () => {
			try {
				const response = await fetch('http://localhost:5000/data');
				const result = await response.json();
				console.log(result);
				setData(result);
			} catch (err) {
				console.log(err);
			}
		};
		fetchData();
	}, []);

	return (
		<>
			<div>
				<h1>Working</h1>
				{data && <pre>{data['name']}</pre>}
			</div>
		</>
	);
}

export default App;
