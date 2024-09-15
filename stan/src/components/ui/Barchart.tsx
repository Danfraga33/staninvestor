import { CardDescription, CardFooter } from './card';
import {
	Bar,
	BarChart,
	Label,
	Rectangle,
	ReferenceLine,
	XAxis,
} from 'recharts';
import {
	ChartContainer,
	ChartTooltip,
	ChartTooltipContent,
} from '@/components//ui/chart';
import {
	Card,
	CardContent,
	CardHeader,
	CardTitle,
} from '@/components//ui/card';
import { useEffect, useState } from 'react';
const Barchart = () => {
	// const [priceData, setPriceData] = useState();
	// useEffect(() => {
	// 	const fetchData = async () => {
	// 		try {
	// 			const response = await fetch('http://localhost:5000/data');
	// 			const result = await response.json();
	// 			console.log(result);
	// 			setPriceData(result);
	// 		} catch (err) {
	// 			console.log(err);
	// 		}
	// 	};
	// 	fetchData();
	// }, []);
	// console.log(priceData);
	return (
		<Card className="lg:max-w-md" x-chunk="charts-01-chunk-0">
			<CardHeader className="space-y-0 pb-2">
				<CardDescription>Volume Chart </CardDescription>
				<CardTitle className="text-4xl tabular-nums">
					12,584{' '}
					<span className="font-sans text-sm font-normal tracking-normal text-muted-foreground">
						steps
					</span>
				</CardTitle>
			</CardHeader>
			<CardContent>
				<ChartContainer
					config={{
						steps: {
							label: 'Steps',
							color: 'hsl(var(--chart-1))',
						},
					}}
				>
					<BarChart
						accessibilityLayer
						margin={{
							left: -4,
							right: -4,
						}}
						// data={priceData['stockData']}
					>
						<Bar
							dataKey="steps"
							fill="var(--color-steps)"
							radius={5}
							fillOpacity={0.6}
							activeBar={<Rectangle fillOpacity={0.8} />}
						/>
						<XAxis
							dataKey="date"
							tickLine={false}
							axisLine={false}
							tickMargin={4}
							tickFormatter={(value) => {
								return new Date(value).toLocaleDateString('en-US', {
									weekday: 'short',
								});
							}}
						/>
						<ChartTooltip
							defaultIndex={2}
							content={
								<ChartTooltipContent
									hideIndicator
									labelFormatter={(value) => {
										return new Date(value).toLocaleDateString('en-US', {
											day: 'numeric',
											month: 'long',
											year: 'numeric',
										});
									}}
								/>
							}
							cursor={false}
						/>
						<ReferenceLine
							y={1200}
							stroke="hsl(var(--muted-foreground))"
							strokeDasharray="3 3"
							strokeWidth={1}
						>
							<Label
								position="insideBottomLeft"
								value="Average Steps"
								offset={10}
								fill="hsl(var(--foreground))"
							/>
							<Label
								position="insideTopLeft"
								value="12,343"
								className="text-lg"
								fill="hsl(var(--foreground))"
								offset={10}
								startOffset={100}
							/>
						</ReferenceLine>
					</BarChart>
				</ChartContainer>
			</CardContent>
			<CardFooter className="flex-col items-start gap-1">
				<CardDescription>
					Over the past 7 days, you have walked{' '}
					<span className="font-medium text-foreground">53,305</span> steps.
				</CardDescription>
				<CardDescription>
					You need <span className="font-medium text-foreground">12,584</span>{' '}
					more steps to reach your goal.
				</CardDescription>
			</CardFooter>
		</Card>
	);
};

export default Barchart;
