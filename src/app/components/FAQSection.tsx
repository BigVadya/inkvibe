import { useState } from 'react'
import FAQItem from './FAQItem'

const faqs = [
	{
		question: 'Больно ли делать татуировку?',
		answer:
			'Болезненность зависит от индивидуального болевого порога и места нанесения. Наши мастера используют современные методы, чтобы сделать процесс максимально комфортным.',
	},
	{
		question: 'Как ухаживать за татуировкой после сеанса?',
		answer:
			'Мы подробно расскажем и дадим памятку по уходу. Важно соблюдать рекомендации по гигиене, использовать заживляющие средства и избегать солнца и воды первые дни.',
	},
	{
		question: 'Можно ли сделать татуировку по своему эскизу?',
		answer:
			'Конечно! Мы работаем как с вашими идеями, так и предлагаем авторские эскизы. Мастер поможет доработать рисунок под ваш стиль и анатомию.',
	},
	{
		question: 'Безопасно ли делать тату у вас?',
		answer:
			'Да, мы строго соблюдаем стерильность: одноразовые расходники, дезинфекция, сертифицированные краски и оборудование.',
	},
	{
		question: 'Сколько стоит татуировка?',
		answer:
			'Цена зависит от размера, сложности и выбранного мастера. Точную стоимость вы узнаете на бесплатной консультации.',
	},
]

export default function FAQSection() {
	const [openIndex, setOpenIndex] = useState<number | null>(null)

	return (
		<section className='bg-white py-16 md:py-24'>
			<div className='container mx-auto px-4'>
				<h2 className='text-3xl md:text-4xl font-bold text-center text-primary mb-12'>
					FAQ
				</h2>
				<div className='max-w-3xl mx-auto'>
					{faqs.map((faq, index) => (
						<FAQItem
							key={index}
							question={faq.question}
							answer={faq.answer}
							isOpen={openIndex === index}
							onClick={() => setOpenIndex(openIndex === index ? null : index)}
						/>
					))}
				</div>
			</div>
		</section>
	)
}
