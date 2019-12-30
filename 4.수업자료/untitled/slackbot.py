from oauth2client.service_account import ServiceAccountCredentials
from httplib2 import Http
from googleapiclient.discovery import build
import slack

attachment_dict = dict()
attachment_dict['pretext'] = ''
attachment_dict['title'] = 'HOW TO USE CS BOT'
attachment_dict['title_link'] = 'https://docs.google.com/spreadsheets/d/10V8_ahKyjNjy7yXxPEbFvou08ZHZJdjiyw41T4ZEZu4/edit#gid=1177088386'
attachment_dict['text'] = '*calculate*=project_name(channel)/Qty/shipping_carrier/country/returnfee\r\n*search*=tracking_number' \
                          '\r\n*send*=project.product,Qty,name,email,phone,detail,city,state,country,zipcode,carrier' \
                          ' \r\n*get* ->customer_name\r\nPROJECT_NAME\r\ndreamcatcher fp -> fp_dc_photobok_2019_Atype/Btype/Ctype\r\npo_dc_2019_normal/limited/set\r\npo_theboyz_normal/po_theboyz_set'
attachment_dict['mrkdwn_in'] = ["text", "pretext"]
attachments = [attachment_dict]

@slack.RTMClient.run_on(event='message')
def say_hello(**payload):
    data = payload['data']                  # 받은메시지의 모든 정보
    if 'bot_id' in data:                    # 봇이 보낸 메시지 일때는 패스
        return

    channel_id = data['channel']            # 받은메시지의 채널 정보(어느 채널에서 왔는가?)
    web_client = payload['web_client']      # 받은메시지에 응답할 때 필요한 정보
    chat = data.get('text', [])             # 받은메시지의 내용
    print(chat)
    if 'calculate' in chat:
        values = [chat.split("/")[1:]]
        print(values)
        fee = calculate(values)
        web_client.chat_postMessage(
                channel=channel_id,
                text= fee,
                attachments = attachments
            )
    elif 'search' in chat:
        status = [chat.split(",")[1:]]
        print(status)
        payment = search(status)
        web_client.chat_postMessage(
            channel=channel_id,
            text= payment,
            attachments=attachments
        )
    elif 'send' in chat:
        info = [chat.split(",")[1:]]
        print(info)
        web_client.chat_postMessage(
            channel=channel_id,
            text="Will request malltail to ship it out",
            attachments=attachments
        )
        return send(info)
    elif 'get' in chat:
        name = [chat.split(",")[1:]]
        print(name)
        tracking_num = get(name)
        web_client.chat_postMessage(
            channel=channel_id,
            text=tracking_num,
            attachments=attachments
        )


def calculate(values):
    body = {'values': values}
    print('cal_body', body)
    write_result = service.spreadsheets().values().update(spreadsheetId=SPREADSHEET_ID ,
                                                     range='Dashboard!A2:E2', #2
                                                     valueInputOption='USER_ENTERED', body=body)

    write_result.execute()

    return read()

def read():
    read_result = service.spreadsheets().values().get(spreadsheetId=SPREADSHEET_ID,
                                                      range='Dashboard!A2:G2').execute()
    answers = read_result.get('values',[])
    if not answers:
        print('No data found.')
    else:
        print('project,quantity,fee:')
        for row in answers:
            fee = ('%s,%s,%s'%(row[0],row[1],row[6]))
            print(fee)
            return fee

def search(status):
    body = {'values': status}
    print('cal_body', body)
    search_result = service.spreadsheets().values().update(spreadsheetId=SPREADSHEET_ID,
                                                          range='Dashboard!A7',  # 2
                                                          valueInputOption='USER_ENTERED', body=body)

    search_result.execute()

    return read2()

def read2():
    read2_result = service.spreadsheets().values().get(spreadsheetId=SPREADSHEET_ID,
                                                      range='Dashboard!A7:C7').execute()
    answers = read2_result.get('values',[])
    if not answers:
        print('No data found.')
    else:
        print('project,quantity,fee:')
        for row in answers:
            payment = ('%s,%s,%s'%(row[0],row[1],row[2]))
            print(payment)
            return payment

def send(info):
    body = {'values': info}
    send_result = service.spreadsheets().values().append(spreadsheetId=SPREADSHEET_ID,
                                                       range = 'SHIPPINGLIST!A1:L1',
                                                       valueInputOption = 'USER_ENTERED',body=body)
    send_result.execute()

def get(name):
    body = {'values':name}
    get_result = service.spreadsheets().values().update(spreadsheetId=SPREADSHEET_ID,
                                                        range = 'DASHBOARD!A10',
                                                        valueInputOption = 'USER_ENTERED',body=body)
    get_result.execute()
    return read3()

def read3():
    read3_result = service.spreadsheets().values().get(spreadsheetId=SPREADSHEET_ID,
                                                       range = 'DASHBOARD!A10:C10').execute()
    answers = read3_result.get('values',[])
    if not answers:
        print('no data found')
    else :
        print('name,status,tracking_num:')
        for row in answers:
            tracking_num = ('%s,%s,%s'%(row[0],row[1],row[2]))
            print(tracking_num)
            return tracking_num

print("start")
if __name__ == '__main__':
    print("init started")
    slack_token = "xoxb-2497510613-856432701953-VL3J4B6NlkyeSgogWsJf72Aa"
    slack_token = "Slacktoken"
    rtm_client = slack.RTMClient(token=slack_token)
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
    SPREADSHEET_ID = '10V8_ahKyjNjy7yXxPEbFvou08ZHZJdjiyw41T4ZEZu4'
    print("init in process")

    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        'C:/Users/MMT/Downloads/My Project 71063-3df5c85644c9.json', SCOPES)
    http_auth = credentials.authorize(Http())
    service = build('sheets', 'v4', http=http_auth)
    print("init finished")

    rtm_client.start()