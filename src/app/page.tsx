'use client'

import Image from 'next/image'
import { useState } from 'react'
import FAQSection from './components/FAQSection'
import FeatureItem from './components/FeatureItem'
import FeatureList from './components/FeatureList'
import Footer from './components/Footer'
import Hero1 from './components/hero/Hero1'
import MobileMenu from './components/MobileMenu'
// import PricingSection from './components/PricingSection'
import TestimonialCard from './components/TestimonialCard'
// import Hero2 from "./components/hero/Hero2";

export default function Home() {
	const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false)

	return (
		<div className='min-h-screen flex flex-col bg-white'>
			<header className='bg-white shadow-sm sticky top-0 z-50'>
				<div className='container mx-auto px-4 py-4 flex justify-between items-center'>
					<a href='#top' className='text-2xl font-bold text-primary'>
						InkVibe
					</a>
					<nav className='hidden md:flex items-center space-x-8'>
						<a
							key='Портфолио'
							href='#portfolio'
							className='text-secondary hover:text-accent transition duration-300'
						>
							Портфолио
						</a>
						<a
							key='Отзывы'
							href='#testimonials'
							className='text-secondary hover:text-accent transition duration-300'
						>
							Отзывы
						</a>
						<a
							href='https://t.me/inkvibe_bot'
							target='_blank'
							rel='noopener noreferrer'
							className='bg-accent text-white px-4 py-2 rounded-md hover:bg-accent/80 transition duration-300'
						>
							Записаться
						</a>
					</nav>
					<button
						className='md:hidden text-secondary hover:text-accent transition duration-300'
						onClick={() => setIsMobileMenuOpen(true)}
					>
						<svg
							xmlns='http://www.w3.org/2000/svg'
							className='h-6 w-6'
							fill='none'
							viewBox='0 0 24 24'
							stroke='currentColor'
						>
							<path
								strokeLinecap='round'
								strokeLinejoin='round'
								strokeWidth={2}
								d='M4 6h16M4 12h16M4 18h16'
							/>
						</svg>
					</button>
				</div>
			</header>

			<MobileMenu
				isOpen={isMobileMenuOpen}
				onClose={() => setIsMobileMenuOpen(false)}
			/>

			<main className='flex-grow container mx-auto px-4 py-12 md:py-24'>
				<Hero1 />
			</main>

			<section className='bg-white py-16 md:py-24'>
				<div className='container mx-auto px-4'>
					<h2 className='text-3xl md:text-4xl font-bold text-center text-primary mb-12'>
						Почему выбирают InkVibe?
					</h2>
					<div className='grid grid-cols-1 md:grid-cols-3 gap-8 md:gap-12'>
						<FeatureItem
							icon={
								<svg
									className='w-12 h-12 text-accent'
									fill='none'
									stroke='currentColor'
									viewBox='0 0 24 24'
									xmlns='http://www.w3.org/2000/svg'
								>
									<path
										strokeLinecap='round'
										strokeLinejoin='round'
										strokeWidth={2}
										d='M12 18h.01M8 21h8a2 2 0 002-2V5a2 2 0 00-2-2H8a2 2 0 00-2 2v14a2 2 0 002 2z'
									/>
								</svg>
							}
							title='Опытные мастера'
							description='Наши мастера — профессионалы с художественным образованием и большим портфолио. Мы подходим к каждому клиенту индивидуально и всегда на связи для консультаций.'
						/>
						<FeatureItem
							icon={
								<svg
									className='w-12 h-12 text-accent'
									fill='none'
									stroke='currentColor'
									viewBox='0 0 24 24'
									xmlns='http://www.w3.org/2000/svg'
								>
									<path
										strokeLinecap='round'
										strokeLinejoin='round'
										strokeWidth={2}
										d='M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z'
									/>
								</svg>
							}
							title='Стерильность и безопасность'
							description='Мы строго соблюдаем стандарты стерильности: используем одноразовые расходники, современное оборудование и сертифицированные материалы.'
						/>
						<FeatureItem
							icon={
								<svg
									className='w-12 h-12 text-accent'
									fill='none'
									stroke='currentColor'
									viewBox='0 0 24 24'
									xmlns='http://www.w3.org/2000/svg'
								>
									<path
										strokeLinecap='round'
										strokeLinejoin='round'
										strokeWidth={2}
										d='M13 10V3L4 14h7v7l9-11h-7z'
									/>
								</svg>
							}
							title='Индивидуальный подход'
							description='Создаём авторские эскизы, учитываем ваши пожелания и особенности. Бесплатная консультация и поддержка на всех этапах — от идеи до заживления.'
						/>
					</div>
				</div>
			</section>

			<section
				id='portfolio'
				className='py-16 md:py-24 overflow-hidden bg-white'
			>
				<div className='container mx-auto px-4'>
					<div className='flex flex-col md:flex-row items-center'>
						<div className='w-full md:w-1/2 mb-12 md:mb-0'>
							<div className='relative'>
								<Image
									src='/images/tatoo2.jpg'
									alt='Tattoo artist at work'
									width={500}
									height={500}
									className='w-full h-auto relative z-10 transform hover:scale-105 transition-transform duration-300'
								/>
							</div>
						</div>
						<div className='w-full md:w-1/2 md:pl-12'>
							<h2 className='text-3xl md:text-4xl font-bold text-accent mb-6 leading-tight'>
								Портфолио работ
							</h2>
							<p className='text-xl text-secondary mb-8 leading-relaxed'>
								Посмотрите лучшие работы наших мастеров и вдохновитесь для своей
								будущей татуировки.
							</p>
							<FeatureList
								items={[
									'Реализм, графика, минимализм и другие стили',
									'Индивидуальные эскизы под ваш запрос',
									'Используем только качественные краски и материалы',
								]}
							/>
						</div>
					</div>
				</div>
			</section>

			<section className='bg-white py-16 md:py-24 overflow-hidden'>
				<div className='container mx-auto px-4'>
					<div className='flex flex-col md:flex-row-reverse items-center'>
						<div className='w-full md:w-1/2 mb-12 md:mb-0'>
							<div className='relative'>
								<Image
									src='/images/tatoo1.jpg'
									alt='Tattoo studio interior'
									width={400}
									height={600}
									className='w-full h-auto relative z-10 transform hover:scale-105 transition-transform duration-300'
								/>
							</div>
						</div>
						<div className='w-full md:w-1/2 md:pr-12'>
							<h2 className='text-3xl md:text-4xl font-bold text-accent mb-6 leading-tight'>
								Уютная атмосфера
							</h2>
							<p className='text-xl text-secondary mb-8 leading-relaxed'>
								Мы заботимся о вашем комфорте: современный интерьер, дружелюбная
								команда и индивидуальный подход к каждому гостю.
							</p>
							<FeatureList
								items={[
									'Приятная музыка и чай/кофе для гостей',
									'Возможность выбрать мастера и время',
									'Детальная консультация по уходу за тату',
								]}
							/>
						</div>
					</div>
				</div>
			</section>
			<section id='testimonials' className='bg-white py-16 md:py-24'>
				<div className='container mx-auto px-4'>
					<h2 className='text-3xl md:text-4xl font-bold text-center text-primary mb-12'>
						Отзывы наших клиентов
					</h2>
					<div className='grid grid-cols-1 md:grid-cols-3 gap-8'>
						<TestimonialCard
							quote='Долго искал своего мастера — теперь советую InkVibe всем друзьям! Крутая атмосфера и профессиональный подход.'
							name='Алексей'
							description='Клиент InkVibe'
							imageSrc='/images/testimonial1.jpg'
						/>
						<TestimonialCard
							quote='Очень понравилось, как сделали мою первую татуировку. Всё стерильно, мастер объяснил все нюансы.'
							name='Мария'
							description='Клиентка InkVibe'
							imageSrc='/images/testimonial3.jpg'
						/>
						<TestimonialCard
							quote='Делал уже третью тату, всегда доволен результатом. Спасибо за индивидуальный подход!'
							name='Игорь'
							description='Постоянный клиент'
							imageSrc='/images/testimonial2.jpg'
						/>
					</div>
				</div>
			</section>
			<FAQSection />
			{/* <PricingSection /> */}
			<section className='bg-white py-20'>
				<div className='container mx-auto px-4 text-center'>
					<p className='text-accent font-semibold mb-4'>
						Запишитесь на бесплатную консультацию
					</p>
					<h2 className='text-4xl md:text-5xl font-bold text-primary mb-8 max-w-4xl mx-auto'>
						Готовы к новой татуировке? Оставьте заявку и мы свяжемся с вами!
					</h2>
					<a
						href='https://t.me/inkvibe_bot'
						target='_blank'
						rel='noopener noreferrer'
						className='bg-accent text-white px-8 py-3 rounded-md text-lg font-semibold hover:bg-accent/80 transition duration-300'
					>
						Записаться
					</a>
				</div>
			</section>
			<Footer />
		</div>
	)
}
