from oauth2client.service_account import ServiceAccountCredentials
from httplib2 import Http
from googleapiclient.discovery import build
import slack

attachment_dict = dict()
attachment_dict['pretext'] = ''
attachment_dict['title'] = 'HOW TO USE CS BOT'
attachment_dict['title_link'] = ''
attachment_dict['text'] = '*calculate* -> project_name(channel),Qty,shipping_carrier,country\r\n*search* -> tracking_number\r\nPROJECT_NAME\r\ndreamcatcher fp -> fp_dc_photobok_2019_Atype/Btype/Ctype'
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
        values = [chat.split(",")[1:]]
        print(values)
        fee = calculate(values)
        web_client.chat_postMessage(
                channel=channel_id,
                text= fee,
                attachments = attachments
            )
    elif 'search' in chat:
        status = [chat.split(",")[1:]]
        print(status)# 만약 chat에 안녕이라는 단어가 포함돼있으면
        payment = search(status)
        web_client.chat_postMessage(        # 답을 한다
            channel=channel_id,
            text= payment,
            attachments=attachments
        )


def calculate(values):
    body = {'values': values}
    print('cal_body', body)
    write_result = service.spreadsheets().values().update(spreadsheetId=SPREADSHEET_ID ,
                                                     range='', #2
                                                     valueInputOption='USER_ENTERED', body=body)

    write_result.execute()

    return read()

def read():
    read_result = service.spreadsheets().values().get(spreadsheetId=SPREADSHEET_ID,
                                                      range='').execute()
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
                                                      range='').execute()
    answers = read2_result.get('values',[])
    if not answers:
        print('No data found.')
    else:
        print('project,quantity,fee:')
        for row in answers:
            payment = ('%s,%s,%s'%(row[0],row[1],row[2]))
            print(payment)
            return payment

print("start")
if __name__ == '__main__':
    print("init started")
    slack_token = "slack_api_token"
    rtm_client = slack.RTMClient(token=slack_token)
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
    SPREADSHEET_ID = 'spreadsheet_id'
    print("init in process")

    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        '', SCOPES)
    http_auth = credentials.authorize(Http())
    service = build('', '', http=http_auth)
    print("init finished")

    rtm_client.start()