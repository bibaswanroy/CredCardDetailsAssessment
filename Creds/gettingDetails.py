import requests
from bs4 import BeautifulSoup
import pandas as pd



#<-------------UNDERSTAND THAT CARDS PRESENT IN THE SBI CREDIT CARDS SECTIONS, AND WHOSE FEES ARE DEPENDENT ON SBI ONLY, OR NOT THROUGH SOME THIRD PARTY SITE ARE LISTED------>

url = 'https://www.sbicard.com/en/personal/credit-cards.page#all'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'lxml')


cards = soup.find_all('div', class_='grid col-2')


cardNames, cardFees, rewards, mileBen, lounges, reversals = [], [], [], [], [], []

for card in cards:
   
    #GETTING THE NAMES

    card_name = card.find('h4', {'style':'color:#222222;'}).get_text(strip=True)
    if card_name not in cardNames:
        cardNames.append(card_name)
        url = card.find('a').get('href')
        new_resp = requests.get(url)
        s = BeautifulSoup(new_resp.text, 'lxml')
        feesplace = s.find('div', {'id' : 'feature-2-tab'})

        #GETTING FEES
        
        if feesplace:
            fees = feesplace.find('ul', class_='sub-list')
            if fees:
                cardFees.append(fees.get_text())
            else:
                cardFees.append('NA')
        else:
            cardFees.append('NA')


        #Getting the region for facilities
        facilities = s.find_all('div', class_='grid col-2') + s.find_all('div', class_='grid col-2 clear-left')

        rew = ''
        bens = ''
        lounge = ''
        rev = ''
        if facilities:
            for fac in facilities:
                #REWARDS


                if 'reward' in fac.find('h3').get_text(strip=True).lower():
                    if fac.find('ul'):
                        rew += fac.find('ul').get_text()
                    if fac.find('div', class_='secondary-view') and fac.find('div', class_='secondary-view').find('ul'):
                        rew += fac.find('div', class_='secondary-view').find('ul').get_text()
                    
                #MILESTONES

                if 'milestone' in fac.find('h3').get_text(strip=True).lower():
                    if fac.find('ul'):
                        bens += fac.find('ul').get_text()
                    if fac.find('div', class_='secondary-view') and fac.find('div', class_='secondary-view').find('ul'):
                        bens += fac.find('div', class_='secondary-view').find('ul').get_text()

                #LOUNGE ACCESS

                if 'lounge' in fac.find('h3').get_text(strip=True).lower():
                    if fac.find('ul'):
                        lounge += fac.find('ul').get_text()


                #FEE REVERSALS
                
                if 'reversal' in fac.find('h3').get_text(strip=True).lower():
                    if fac.find('ul'):
                        rev += fac.find('ul').get_text()
                    
                
        rewards.append(rew) if rew != '' else rewards.append('NA')
        mileBen.append(bens) if bens != '' else mileBen.append('NA')
        lounges.append(lounge) if lounge != '' else lounges.append('NA')
        reversals.append(rev) if rev != '' else reversals.append('NA')

df = pd.DataFrame({'Card Name': cardNames,
                    'Card Fees': cardFees,
                    'Reward Points': rewards,
                    'Lounge Access': lounges,
                    'Milestone Benefits': mileBen,
                    'Fee Reversal Condition': reversals})

df.to_excel('CardDetails.xlsx', index=False)

