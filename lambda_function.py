import os
import requests
import json

def call_openai_api(user_message: str) -> str:
    """
    OpenAI API 호출 함수
    Args:
        user_message (str): 사용자로부터 입력받은 메시지
    Returns:
        str: OpenAI API의 응답 메시지
    """
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("Error: 'OPENAI_API_KEY' 환경 변수가 설정되지 않았습니다.")
        raise ValueError("환경 변수 'OPENAI_API_KEY'가 설정되지 않았습니다.")
    
    api_url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    # 대화 맥락을 포함한 메시지 리스트
    messages = [
        {"role": "system", "content": "너는 친절하고 도움이 되는 챗봇입니다."},
        {"role": "user", "content": user_message}
    ]

    payload = {
        "model": "gpt-3.5-turbo",
        "messages": messages,
        "max_tokens": 150,
        "temperature": 0.7  # 높은 창의성의 응답을 위해 조정
    }

    print(f"Sending request to OpenAI API with message: {user_message}")

    try:
        response = requests.post(api_url, headers=headers, json=payload)
        print(f"API response status: {response.status_code}")
        
        if response.ok:
            data = response.json()
            message = data.get('choices', [{}])[0].get('message', {}).get('content', "응답 처리 실패")
            return message.strip()  # 응답의 양쪽 공백 제거
        else:
            print(f"Error in API response: {response.text}")
            return "죄송합니다. 유효한 응답을 받지 못했습니다."
    except requests.exceptions.RequestException as e:
        print(f"Error during API call: {str(e)}")
        return "죄송합니다. API 호출 중 오류가 발생했습니다."

def lambda_handler(event, context):
    """
    AWS Lambda 핸들러
    Args:
        event (dict): 이벤트 데이터 (API Gateway에서 전달)
        context (object): Lambda 실행 컨텍스트
    Returns:
        dict: API Gateway로 반환할 HTTP 응답
    """
    print("Received event:", json.dumps(event))
    
    try:
        user_message = event.get('user', {}).get('message', '안녕하세요!')
    except Exception as e:
        print(f"Error parsing user message: {str(e)}")
        user_message = '안녕하세요!'
    
    print("User message:", user_message)
    
    try:
        response_message = call_openai_api(user_message)
    except Exception as e:
        print(f"Error calling OpenAI API: {str(e)}")
        response_message = "죄송합니다. API 호출 중 오류가 발생했습니다."
    
    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*"
        },
        "body": json.dumps({'response': response_message})
    }
