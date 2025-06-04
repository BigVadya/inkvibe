import Link from 'next/link'
import React from 'react'

const Footer: React.FC = () => {
	return (
		<footer className='bg-primary py-12 md:py-16'>
			<div className='container mx-auto px-4'>
				<div className='grid grid-cols-1 md:grid-cols-12 gap-8'>
					{/* Company Info */}
					<div className='md:col-span-3 mb-8 md:mb-0'>
						<Link
							href='/'
							className='text-2xl font-bold text-accent hover:text-accent/80 transition duration-300'
						>
							InkVibe
						</Link>
						<p className='mt-4 text-sm text-secondary'>
							InkVibe — современный тату-салон. Уникальные татуировки, опытные
							мастера, стерильность и уютная атмосфера.
						</p>
					</div>
				</div>

				{/* Copyright */}
				<div className='mt-8 pt-8 border-t border-secondary text-center text-sm text-secondary'>
					<p>
						&copy; {new Date().getFullYear()} InkVibe, Inc. All rights reserved.
					</p>
				</div>
			</div>
		</footer>
	)
}

export default Footer
