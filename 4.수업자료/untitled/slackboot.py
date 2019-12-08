

credentials = ServiceAccountCredentials.from_json_keyfile_name('C:/Users/MMT/Downloads/My Project 71063-3df5c85644c9.json',SCOPES)
http_auth = credentials.authorize(Http())
service = build('sheets','v4',http= http_auth)


    credentials = ServiceAccountCredentials.from_json_keyfile_name('C:/Users/MMT/Downloads/My Project 71063-3df5c85644c9.json',SCOPES)

    http_auth = credentials.authorize(Http())

def event_handler(event_type, slack_event):
    if event_type == "app_mention":
        say_hello()

@slack.RTMClient.run_on(event='message')
def say_hello(**payload):
    data = payload['data']                  # 받은메시지의 모든 정보
    if 'bot_id' in data:                    # 봇이 보낸 메시지 일때는 패스
        return

    channel_id = data['channel']            # 받은메시지의 채널 정보(어느 채널에서 왔는가?)
    web_client = payload['web_client']      # 받은메시지에 응답할 때 필요한 정보

    chat = data.get('text', [])             # 받은메시지의 내용
    if 'calculate' in chat:
        values = chat.split(",")[1:]
        print(values)# 만약 chat에 hello라는 단어가 포함돼있으면
        web_client.chat_postMessage(        # 답을 한다
                channel=channel_id,
                text= abs
            )
    elif '안녕' in chat:                     # 만약 chat에 안녕이라는 단어가 포함돼있으면
        web_client.chat_postMessage(        # 답을 한다
            channel=channel_id,
            text='한국인이세요?'
        )
    else:                                   # 이도저도 아니면
        web_client.chat_postMessage(        # 답을 한다
            channel=channel_id,
            text='무슨 말인지 모르겠어요!'
        )
    return values

def google_cal(user_input = None):
    body = {'values': user_input}
    read_result = service.spreadsheets().values().get(spreadsheetId=SPREADSHEET_ID,
                                                      range='Dashboard!A2:G2').execute()
    answers = user_input['values']
    if not answers:
        print('No data found.')
    else:
        print('project,quantity,fee:')
        for row in answers:
            a = ('%s,%s,%s' % (row[0], row[1], row[6]))
            print(a)

    write_result = service.spreadsheets().values().update(spreadsheetId=SPREADSHEET_ID,
                                                          range='Dashboard!A2:D2',  # 2
                                                          valueInputOption='RAW', body=body)
    write_result.execute()
    return values


slack_input = say_hello()
google_cal(slack_input)