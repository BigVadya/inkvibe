import Image from 'next/image'

function TestimonialCard({
	quote,
	name,
	description,
	imageSrc,
}: {
	quote: string
	name: string
	description: string
	imageSrc: string
}) {
	return (
		<div className='bg-white p-8 rounded-lg shadow-md transition-all duration-300 hover:shadow-xl'>
			<div className='flex items-center mb-6'>
				<div className='w-16 h-16 mr-4 relative overflow-hidden rounded-full'>
					<Image src={imageSrc} alt={name} layout='fill' objectFit='cover' />
				</div>
				<div>
					<h4 className='font-semibold text-gray-800 text-lg'>{name}</h4>
					<p className='text-sm text-gray-600'>{description}</p>
				</div>
			</div>
			<p className='text-accent mb-6 leading-relaxed italic'>{quote}</p>
		</div>
	)
}

export default TestimonialCard
