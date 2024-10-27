import { get_chats, start_chat, continue_chat,  } from './apiService.js'
import { getItemFromSessionStorage } from './utils.js'
export const getAllPreviousChats = async() => {
    const previousChatsContainer = document.getElementById('chat-categories')
    const data = await get_chats()
    const chats = data.data
    if (chats){
        //success render data
    }
}

const renderChats = (chats, new_chat) => {
    console.log(chats)
    const aiBox = document.getElementById('ai-box')
    const hideOnChatMode = document.querySelectorAll('.hidden')
    const chatMessages = document.getElementById('chat-messages')
    const userData = getItemFromSessionStorage("user")
    const userFirstName = userData["firstname"]
    if (new_chat){
        aiBox.classList.add('chat-mode')
        hideOnChatMode.forEach(hcm => hcm.classList.add('cm_no__show'))
    }   
    
    let x = 1
    let user = userFirstName[0].toUpperCase()
    while (x <= chats.length){
        let selection = x % 2
        let child = null
        if (selection == 1){
            child = createMessageElement('user-prompt','profile_person', user, chats[x - 1])
        }else {
            child = createMessageElement('ai-response','profile_ai', 'R', chats[x - 1])
        }
        chatMessages.append(child)
        x++;
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
        return mainDiv
    }

    
}
export const chat = () => {
    const PATH_LENGTH = 3
    form.addEventListener('submit', async (e) => {
        const form = document.getElementById('AI')
        const formData = new FormData(form)
        let prompt = formData.get('AI')
        e.preventDefault()

        const urlPath = window.location.pathname
        const paths = urlPath.split('/')
        if (paths.length === PATH_LENGTH){
            // continue that chat

            const chatId = paths[2]
            const response = await continue_chat(prompt, chatId)
            const data = response.data
            const aiResponse = data["response"]
            renderChats([prompt,aiResponse["response"]], false)
            return
        }
    
        const response  = await start_chat(prompt)

        console.log(response)
        const data = response.data
        const aiResponse = data["response"]
        const conversationId = data["conversation_id"]
        history.pushState(null, '', `/${conversationId}`)
        renderChats([prompt, aiResponse["response"]], true)
    })

}