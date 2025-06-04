import React from 'react'

interface MobileMenuProps {
	isOpen: boolean
	onClose: () => void
}

const MobileMenu: React.FC<MobileMenuProps> = ({ isOpen, onClose }) => {
	if (!isOpen) return null

	return (
		<div className='fixed inset-0 bg-primary bg-opacity-75 z-50'>
			<div className='fixed inset-y-0 right-0 max-w-xs w-full bg-white shadow-xl z-50'>
				<div className='flex justify-end p-4'>
					<button
						onClick={onClose}
						className='text-secondary hover:text-secondary'
					>
						<svg
							className='h-6 w-6'
							fill='none'
							viewBox='0 0 24 24'
							stroke='currentColor'
						>
							<path
								strokeLinecap='round'
								strokeLinejoin='round'
								strokeWidth={2}
								d='M6 18L18 6M6 6l12 12'
							/>
						</svg>
					</button>
				</div>
				<nav className='px-4 py-2'>
					<a
						href='#portfolio'
						className='block py-2 text-secondary hover:text-accent transition duration-300'
						onClick={onClose}
					>
						Портфолио
					</a>
					<a
						href='#testimonials'
						className='block py-2 text-secondary hover:text-accent transition duration-300'
						onClick={onClose}
					>
						Отзывы
					</a>
					<a
						href='https://t.me/inkvibe_bot'
						target='_blank'
						rel='noopener noreferrer'
						className='w-full mt-4 bg-accent text-white px-4 py-2 rounded-md hover:bg-accent/80 transition duration-300 block text-center'
						onClick={onClose}
					>
						Записаться
					</a>
				</nav>
			</div>
		</div>
	)
}

export default MobileMenu
