# -*- coding: utf-8 -*-
"""resumeText&describeImg.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1X-XHUUBKFFVaZmzPC62kQSFxE1ybwE57
"""

!pip install transformers

!pip install timm

from transformers import pipeline

# Aplicación 1
clasificacion_imagenes = pipeline(task = "image-classification")

clasificacion_imagenes("/content/Screenshot 2023-09-04 at 4.59.00 p.m..png")

import timm

segmentacion_imagenes = pipeline(task="image-segmentation")

segmentacion_imagenes("/content/Screenshot 2023-09-04 at 4.59.00 p.m..png")

# Aplicaciones de texto
sum = pipeline(task = "summarization")

texto = '''Meta Platforms, Inc.,[15][16] doing business as Meta,[17][18] and formerly named Facebook, Inc., and TheFacebook, Inc.,[19] is an American multinational technology conglomerate based in Menlo Park, California. The company owns and operates Facebook, Instagram, Threads, and WhatsApp, among other products and services.[20] Meta is one of the world's most valuable companies and among the ten largest publicly traded corporations in the United States.[21] It is considered one of the Big Five American information technology companies, alongside Google's parent company Alphabet, Amazon, Apple, and Microsoft.

In addition to Facebook, Instagram, Threads and WhatsApp, Meta has also acquired Oculus (which it has integrated into Reality Labs), Mapillary, CTRL-Labs, and has a 9.99% stake in Jio Platforms; the company additionally endeavored into non-VR hardware such as the discontinued Meta Portal smart displays line and presently partners with Luxottica through the Ray-Ban Stories series of smart glasses.[22][23] Despite endeavors into hardware, the company still relies on advertising for a vast majority of its revenue, which in 2022 made up 97.5 percent of its revenue.[12]

On October 28, 2021, the parent company of Facebook changed its name from Facebook, Inc., to Meta Platforms, Inc., to "reflect its focus on building the metaverse".[24] According to Meta, the term "metaverse" refers to the integrated environment that links all of the company's products and services.History
Further information: History of Facebook and Initial public offering of Facebook

Billboard on the Thomson Reuters building welcomes Facebook to Nasdaq, 2012

Facebook filed for an initial public offering (IPO) on January 1, 2012.[28] The preliminary prospectus stated that the company sought to raise $5 billion, had 845 million monthly active users, and a website accruing 2.7 billion likes and comments daily.[29] After the IPO, Zuckerberg would retain a 22% ownership share in Facebook and would own 57% of the voting shares.[30]

Underwriters valued the shares at $38 each, valuing the company at $104 billion, the largest valuation to date for a newly public company.[31] On May 16, one day before the IPO, Facebook announced it would sell 25% more shares than originally planned due to high demand.[32] The IPO raised $16 billion, making it the third-largest in US history (slightly ahead of AT&T Wireless and behind only General Motors and Visa). The stock price left the company with a higher market capitalization than all but a few U.S. corporations—surpassing heavyweights such as Amazon, McDonald's, Disney, and Kraft Foods—and made Zuckerberg's stock worth $19 billion.[33][34] The New York Times stated that the offering overcame questions about Facebook's difficulties in attracting advertisers to transform the company into a "must-own stock". Jimmy Lee of JPMorgan Chase described it as "the next great blue-chip".[33] Writers at TechCrunch, on the other hand, expressed skepticism, stating, "That's a big multiple to live up to, and Facebook will likely need to add bold new revenue streams to justify the mammoth valuation."[35]

Trading in the stock, which began on May 18, was delayed that day due to technical problems with the Nasdaq exchange.[36] The stock struggled to stay above the IPO price for most of the day, forcing underwriters to buy back shares to support the price.[37] At closing bell, shares were valued at $38.23,[38] only $0.23 above the IPO price and down $3.82 from the opening bell value. The opening was widely described by the financial press as a disappointment.[39] The stock nonetheless set a new record for trading volume of an IPO.[40] On May 25, 2012, the stock ended its first full week of trading at $31.91, a 16.5% decline.[41]

On May 22, 2012, regulators from Wall Street's Financial Industry Regulatory Authority announced that they had begun to investigate whether banks underwriting Facebook had improperly shared information only with select clients rather than the general public. Massachusetts Secretary of State William Galvin subpoenaed Morgan Stanley over the same issue.[42] The allegations sparked "fury" among some investors and led to the immediate filing of several lawsuits, one of them a class action suit claiming more than $2.5 billion in losses due to the IPO.[43] Bloomberg estimated that retail investors may have lost approximately $630 million on Facebook stock since its debut.[44] Standard & Poor's added Facebook to its S&P 500 index on December 21, 2013.[45]

On May 2, 2014, Zuckerberg announced that the company would be changing its internal motto from "Move fast and break things" to "Move fast with stable infrastructure".[46][47] The earlier motto had been described as Zuckerberg's "prime directive to his developers and team" in a 2009 interview in Business Insider, in which he also said, "Unless you are breaking stuff, you are not moving fast enough.[48 '''

sum(texto, min_length = 20)

sum_es = pipeline(
    task = "summarization",
    model = "IIC/mt5-spanish-mlsum"
)

texto = """ Visiblemente contento y luciendo una bufanda con la leyenda "Arriba el Monterrey", Corona fue recibido por familiares, miembros de la prensa y cerca de unos 10 aficionados en el Aeropuerto.

"Tengo sentimientos encontrados, la verdad que estoy muy feliz de estar aquí. Esperé unos años por volver y hoy se concretó, así que muy contento y muy ilusionado", dijo al atender a la prensa.

Corona agradeció la confianza y aseguró querer devolverla mediante su buen desempeño.
"Voy a intentar, voy a hacer todo lo posible por regresarles toda la confianza que me tuvieron y esperemos ser muy felices".

El "Tecatito" firmó con los Rayados por los próximos 4 años."""

sum_es(texto, min_length = 20, max_length = 100)

# Aplicar función de sentimiento
sentimiento = pipeline(task = "text-classification", model = "pysentimiento/robertuito-sentiment-analysis")