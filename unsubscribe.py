import mailbox
import re
from selenium import webdriver 
from selenium.webdriver.chrome.options import Options

def get_senders(path):
    senders = {}
    for message in mailbox.mbox(path):
        if 'List-Unsubscribe' in message:
            senders[message['From']] = message['List-Unsubscribe']
    return senders

def open_link(link):
    try:
        if re.search(r'(\<)([https{0,1}].+)(\>)', link):
            driver = webdriver.Chrome(options=options)
            driver.get(link.strip('\<\>'))
        else:
            print(link)
    except:
        print('Chrome webdriver not installed')

def prompt(senders):
    for sender in senders:
        name = re.match(r'(\"{0,1})(\w+)(\w+)?(\"{0,1})(\s\<.+\@.+\.com\>){0,1}', sender).group(2)
        choice = input(f'Do you wish to unsubscribe from emails sent by {name}? ')
        if choice.lower() in ['y', 'yes']:
            open_link(senders[sender])
        if choice.lower() == 'exit':
            exit()

if __name__ == '__main__':
    senders = get_senders('./mail.mbox')
    prompt(senders)