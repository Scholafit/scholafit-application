
export const saveToSessionStorage = (key, value) => {
    sessionStorage.setItem(key, JSON.stringify(value))
}

export const getItemFromSessionStorage = (key) => {
    return JSON.parse(sessionStorage.getItem(key))
}

export const removeItemFromStorage = (key) => {
    sessionStorage.removeItem(key)
}

export const titleCase = (words) => {

    return words.split(' ').map((word) => word.charAt(0).toUpperCase() + word.slice(1)).join(' ')
}


const nav = document.getElementById('nav')
const menu = document.getElementById('mobile-menu')
export const toggleMobileMenu = () => {
    
    nav.addEventListener('click', (e) => {
        if (e.target.classList.contains('open-btn')){
            menu.classList.add('open-menu')
            menu.classList.remove('close-menu')
            return
        }

        if (e.target.classList.contains('close-btn')){
            menu.classList.remove('open-menu')
            menu.classList.add('close-menu')
        }
    })
}
