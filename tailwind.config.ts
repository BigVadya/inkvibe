import type { Config } from 'tailwindcss'

const config: Config = {
	content: [
		'./src/pages/**/*.{js,ts,jsx,tsx,mdx}',
		'./src/components/**/*.{js,ts,jsx,tsx,mdx}',
		'./src/app/**/*.{js,ts,jsx,tsx,mdx}',
	],
	theme: {
		extend: {
			colors: {
				primary: '#111111',
				secondary: '#232323',
				accent: '#b3132b',
				white: '#ffffff',
				black: '#000000',
			},
		},
	},
	plugins: [],
}
export default config
