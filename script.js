document.getElementById('send-button').addEventListener('click', sendMessage);
document.getElementById('user-input').addEventListener('keypress', function (e) {
    if (e.key === 'Enter') {
        sendMessage();
    }
});

async function sendMessage() {
    const userInput = document.getElementById('user-input');
    const message = userInput.value.trim();
    if (!message) return;

    // 사용자 메시지 표시
    appendMessage('user', message);
    userInput.value = '';

    // 로딩 인디케이터 표시
    const loadingDiv = document.createElement('div');
    loadingDiv.className = 'typing-indicator';
    loadingDiv.innerHTML = '<span></span><span></span><span></span>';
    document.getElementById('chat-messages').appendChild(loadingDiv);

    try {
        const apiUrl = '';
        console.log(`Sending POST request to: ${apiUrl}`); // 디버깅: 요청 URL 출력

        const response = await fetch(apiUrl, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                user: {
                    message: message,
                },
            }),
        });

        loadingDiv.remove();

        console.log(`Response status: ${response.status}`); // 디버깅: 응답 상태 출력

        if (response.ok) {
            const data = await response.json();
            console.log('API Response:', data); // 디버깅: API 응답 데이터 출력
            appendMessage('bot', data.response);
        } else {
            console.error('Response error:', response.statusText); // 디버깅: 응답 오류 메시지
            appendMessage('bot', '죄송합니다. 오류가 발생했습니다.');
        }
    } catch (error) {
        loadingDiv.remove();
        console.error('Fetch error:', error); // 디버깅: 요청 실패 오류 출력
        appendMessage('bot', '죄송합니다. 오류가 발생했습니다.');
    }
}

function appendMessage(sender, message) {
    const chatMessages = document.getElementById('chat-messages');
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${sender}`;

    // XSS 방지를 위한 이스케이프 처리
    const escapedMessage = message
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;')
        .replace(/'/g, '&#039;')
        .replace(/\n/g, '<br>');

    messageDiv.innerHTML = escapedMessage;
    chatMessages.appendChild(messageDiv);

    // 부드러운 스크롤 효과
    chatMessages.scrollTo({
        top: chatMessages.scrollHeight,
        behavior: 'smooth',
    });
}

// 초기 웰컴 메시지
window.onload = function () {
    appendMessage('bot', '안녕하세요! 무엇을 도와드릴까요? 😊');
};
