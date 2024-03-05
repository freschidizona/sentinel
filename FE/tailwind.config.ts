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
        'neomorphism': '#f1f3f6',
      },
      backgroundImage: {
        'gradient-radial': 'radial-gradient(var(--tw-gradient-stops))',
        'gradient-conic': 'conic-gradient(from 180deg at 50% 50%, var(--tw-gradient-stops))',
      },
      boxShadow: {
        'neo': '10px 10px 15px #d9d9d9, -10px -10px 15px #f0f0f0',
        'inner-neo': 'inset 5px 5px 10px #d9d9d9, inset -5px -5px 10px #f0f0f0',
      }
    },
  },
  plugins: [],
}
export default config
