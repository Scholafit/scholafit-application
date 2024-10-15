


export const saveToSessionStorage = (key, value) => {
    sessionStorage.setItem(key, JSON.stringify(value))
}

export const getItemFromSessionStorage = (key) => {
    return JSON.parse(sessionStorage.getItem(key))
}

export const removeItemFromStorage = (key) => {
    sessionStorage.removeItem(key)
}