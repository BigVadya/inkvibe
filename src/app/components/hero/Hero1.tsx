import Image from 'next/image'

export default function Hero1() {
	return (
		<div className='flex flex-col md:flex-row items-center'>
			<div id='top'></div>
			<div className='w-full md:w-1/2 pr-0 md:pr-12 mb-8 md:mb-0'>
				<h1 className='text-4xl md:text-5xl lg:text-6xl font-bold text-primary mb-6 leading-tight'>
					InkVibe
				</h1>

				<p className='text-xl text-secondary mb-8 leading-relaxed'>
					InkVibe — современный тату-салон в самом сердце города. Мы создаём
					уникальные татуировки, отражающие вашу индивидуальность. Опытные
					мастера, стерильность, авторские эскизы и уютная атмосфера — всё для
					того, чтобы ваш опыт был не только безопасным, но и вдохновляющим.
				</p>
				<div className='flex items-center space-x-4'>
					<a
						className='bg-accent text-white px-8 py-3 rounded-md hover:bg-accent/80 transition duration-300 shadow-lg'
						href='https://t.me/inkvibe_bot'
						target='_blank'
						rel='noopener noreferrer'
					>
						Записаться
					</a>
					<p className='text-sm text-secondary'>
						С нами 5000+ довольных клиентов
					</p>
				</div>
			</div>
			<div className='w-full md:w-1/2'>
				<Image
					src='/images/heroimage.jpg'
					alt='ACME Solutions Illustration'
					width={600}
					height={600}
					className='w-full h-auto'
				/>
			</div>
		</div>
	)
}
