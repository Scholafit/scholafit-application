import { get_chats, start_chat, continue_chat,  } from './apiService.js'
import { getItemFromSessionStorage } from './utils.js'

const userData = getItemFromSessionStorage("user")
const userFirstName = userData["firstname"]
const aiBox = document.getElementById('ai-box')
const hideOnChatMode = document.querySelectorAll('.hidden')
const textArea = document.getElementById('textArea')
const form = document.getElementById('AI')


export const getAllPreviousChats = async() => {
    const previousChatsContainer = document.getElementById('chat-categories')
    const data = await get_chats()
    const chats = data.data
    if (chats){
        //success render data
    }
}


const updateChatSideBar = ()=> {
    // update the sidebar with data from previous chat
    // update sidebar with new data from new chat
}
const createMessageElement = (mainClass, outerClassB, userSign, msg) => {
    const outerDiv = document.createElement('div')
    outerDiv.classList.add('profile', outerClassB)
    const innerDiv = document.createElement('div')
    const msgDiv = document.createElement('div')
    msgDiv.classList.add('msg')
    
    innerDiv.textContent = userSign
    msgDiv.textContent = msg

    outerDiv.append(innerDiv)

    const mainDiv = document.createElement('div')
    mainDiv.classList.add(mainClass,'message')
    mainDiv.append(outerDiv)
    mainDiv.append(msgDiv)
    const messageContainer = document.createElement('div')
    messageContainer.append(mainDiv)
    return messageContainer
}

const renderChats = (chat_msg,new_chat=false) => {
    
    const chatMessages = document.getElementById('chat-messages')
    const parentContainer = document.getElementById('personalised-wrapper')
    
    if (new_chat){
        aiBox.classList.add('chat-mode')
        hideOnChatMode.forEach(hcm => hcm.classList.add('cm_no__show'))
    }   
   
    chatMessages.append(chat_msg)
    
    parentContainer.scrollTo({
        top: chatMessages.scrollHeight,
        behavior: "smooth"
    })
}

const streamChat = (response) => {
    const text = response["response"]
    const textContainers = document.querySelectorAll('.msg')
    let container = null
    textContainers.forEach(textContainer => {
        if (textContainer.textContent == ''){
            container = textContainer
        }
    })
    let x = 0
    const intervalId = setInterval(()=> {
        if (container && x < text.length){
            container.append(text[x])
            x++;
        }else {
            clearInterval(intervalId)
        }
    }, 10)
    
}


export const chat = () => {
    const PATH_LENGTH = 4
    const submit = async ()=> {
        const formData = new FormData(form)
        let prompt = formData.get('AI')
        textArea.value = ''
        const urlPath = window.location.pathname
        const paths = urlPath.split('/')
        let userChat = createMessageElement('user-prompt','profile_person', userFirstName[0].toUpperCase(), prompt)
        let aiChat = createMessageElement('ai-response','profile_ai', 'R', '')
        const loader = aiChat.querySelector('.profile_ai')
        loader.classList.add('loading')

        if (paths.length === PATH_LENGTH){
            renderChats(userChat)
            renderChats(aiChat)
            const chatId = paths[3]
            const response = await continue_chat(prompt, chatId)
            console.log(response)
            const data = response.data
            const aiResponse = data["response"]
            loader.classList.remove('loading')
            streamChat(aiResponse)
            return
        }

        renderChats(userChat, true)
        renderChats(aiChat)
        const response  = await start_chat(prompt)
        console.log(response)
        const data = response.data
        const aiResponse = data["response"]
        const conversationId = data["conversation_id"]
        loader.classList.remove('loading')
        streamChat(aiResponse)
        history.pushState(null, '', `/personalised.html/chat/${conversationId}`)
    }

    form.addEventListener('submit', async (e) => {
        e.preventDefault()
        await submit()
    })

}

const newChatBtn = document.getElementById('startNewChat')

newChatBtn.addEventListener('click', (e) => {
    const chatMessages = document.getElementById('chat-messages')
    chatMessages.replaceChildren()
    aiBox.classList.remove('chat-mode')
    hideOnChatMode.forEach(hcm => hcm.classList.remove('cm_no__show'))
    textArea.value = ''
    history.replaceState({}, '', '/personalised.html')
})

const getScrollHeight = (el) => {
    let savedVal = el.value
    el.value = ''
    el._baseScrollHeight = el.scrollHeight
    el.value = savedVal
}

const expandTextArea = ({ target: el}) => {
    let minRows = el.getAttribute('data-min-rows') | 0, rows;
    !el._baseScrollHeight && getScrollHeight(el)
    el.rows = minRows
    rows = Math.ceil((el.scrollHeight - el._baseScrollHeight)/ 16)
    el.rows = minRows + rows
}


textArea.addEventListener('input', expandTextArea)

