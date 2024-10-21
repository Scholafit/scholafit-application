
export const saveToSessionStorage = (key, value) => {
    sessionStorage.setItem(key, JSON.stringify(value))
}

export const getItemFromSessionStorage = (key) => {
    return JSON.parse(sessionStorage.getItem(key))
}

export const removeItemFromStorage = (key) => {
    sessionStorage.removeItem(key)
}


const nav = document.getElementById('nav')
const menu = document.getElementById('mobile-menu')
export const toggleMobileMenu = () => {
    
    nav.addEventListener('click', (e) => {
        if (e.target.classList.contains('open-btn')){
            menu.classList.add('open-menu')
            return
        }

        if (e.target.classList.contains('close-btn')){
            menu.classList.remove('open-menu')
        }
    })
}
