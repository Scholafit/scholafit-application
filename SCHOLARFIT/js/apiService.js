const BASE_URL = 'https:/api/v1'

import {getItemFromSessionStorage} from './utils.js'
const createOptions = (requestType, body="")=>{
    const options = {
      method: requestType,
      headers: {
        'Content-Type': 'application/json'
      }
    }
  
    if (body != "") {
      options["body"] = JSON.stringify(body)
    }
    return options
  }

const sendRequest = async (url, options) => {
    const response = await fetch(url, options)
    return response
}


export const signUp = async (userData) => {
    const url = BASE_URL + '/users'
    const options = createOptions('POST', userData)

    try {
      const response = await sendRequest(url, options)
      if (response.status !== 201){
        return {
          status: response.status,
          data: null,
          error: await response.json()
        }
      }
      return {
        status: response.status,
        data: await response.json(),
        error: null
      }
    } catch (err) {
      return {
        status: 500,
        data: null,
        error: err
      }
    }
}


export const login = async (credentials) => {
  const url = BASE_URL + '/login'
    const options = createOptions('POST', credentials)

    try {
      const response = await sendRequest(url, options)
      if (response.status !== 200){
        return {
          status: response.status,
          data: null,
          error: await response.json()
        }
      }
      return {
        status: response.status,
        data: await response.json(),
        error: null
      }
    } catch (err) {
      return {
        status: 500,
        data: null,
        error: err
      }
    }
}

export const updateUserProfile = async (profileId, data) => {
  const url = BASE_URL + `/learner-center/learner-profile/${profileId}`
  const options = createOptions('POST', data)
  try {
    const response = await sendRequest(url, options)
    if (response.status !== 200) {
        const err = await response.json()
        console.log(err)
        return {
            status: response.status,
            data: null,
            error: err
        }
    }
   const resp = await response.json()
   console.log(resp)
   const data = resp["response"]
    return {
        status: response.status,
        data: data,
        error: null
    }
    
  } catch (err) {
    return {
        status: 500,
        data: null,
        error: err
    }
  }
}

export const fetchSubjects = async ()=> {
    const url = BASE_URL + '/learner-center/subjects'
    const options = createOptions('GET')
    try {
        const response = await sendRequest(url, options)
        if (response.status !== 200) {
            const err = await response.json()
            console.log(err)
            return {
                status: response.status,
                data: null,
                error: err
            }
        }
       const resp = await response.json()
       const data = resp["subjects"]
        return {
            status: response.status,
            data: data,
            error: null
        }
        
    } catch (err) {
        return {
            status: 500,
            data: null,
            error: err
        }
    }
    
  }

export const generate_test = async (profile_id) => {
  const url = BASE_URL + `/learner-center/tests/${profile_id}`
  const options = createOptions('POST')

  try {
      const response = await sendRequest(url, options)
      if (response.status != 200){
        const err = await response.json()
        return {
          status: response.status,
          data: null,
          error: err
        }
      }

      return {
        status: response.status,
        data: await response.json(),
        error: null
      }
  } catch (err) {
      return {
        status: 500,
        data: null,
        error: err
      }
  }
}

export const submitTest = async (test_id) => {
  const url = BASE_URL + `/learner-center/tests/submit/${test_id}`
  const answers = getItemFromSessionStorage("answers")
  const arrayAnswers = []
  for (const [key, val] of Object.entries(answers)){
   
    arrayAnswers.push(parseInt(val))
  }
  const body = {"answers": JSON.stringify(arrayAnswers)}
  const options = createOptions('POST', body)
  try {
      const response = await sendRequest(url,options)
      if (response.status !== 200){
        const err = await response.json()
        return {
          status: response.status,
          data: null,
          error: err
        }
      }

      return {
        status: response.status,
        data: await response.json(),
        error: null
      }
  } catch (err) {
      return {
        status: 500,
        data: null,
        error: err
      }
  }
}

export const get_chats = async () => {
  const url = BASE_URL + '/learner-center/ai'
  const options = createOptions('GET')
  try {
      const response = await sendRequest(url, options)
      if (response.status === 200){
        return {
          status: response.status,
          data: await response.json(),
          error: null
        }
      }
      return {
        status: response.status,
        data: null,
        error: await response.json()
      }
  } catch (err) {
      return {
        status: 500,
        data: null,
        error: err
    }
  }
}
export const start_chat = async (promptText) => {
  const url = BASE_URL + '/learner-center/ai'
  const options = createOptions('POST', {"message": promptText})
  try {
      const response = await sendRequest(url, options)
      if (response.status === 201){
        return {
          status: response.status,
          data: await response.json(),
          error: null
        }

      }
      return {
        status: response.status,
        data: null,
        error: await response.json()
      }
      
  } catch (err) {
      return {
        status: 500,
        data: null,
        error: err
    }
  }
}

export const continue_chat = async (promptText, conversationId) => {
  const url = BASE_URL + `/learner-center/ai/${conversationId}`
  const options = createOptions('POST',{"message": promptText})
  try {
      const response = await sendRequest(url, options)
      if (response.status === 200){
        return {
          status: response.status,
          data: await response.json(),
          error: null
        }

      }
      return {
        status: response.status,
        data: null,
        error: await response.json()
      }
      
  } catch (err) {
      return {
        status: 500,
        data: null,
        error: err
    }
  }
}

export const subscribe = async (payment_details) => {
  const url = BASE_URL + '/payments/top-up'
    const options = createOptions('POST', payment_details)

    try {
      const response = await sendRequest(url, options)
      if (response.status !== 200){
        return {
          status: response.status,
          data: null,
          error: await response.json()
        }
      }
      return {
        status: response.status,
        data: await response.json(),
        error: null
      }
    } catch (err) {
      return {
        status: 500,
        data: null,
        error: err
      }
    }
}

export const verifyPayment = async ()=> {
  const reference = getItemFromSessionStorage("reference")
  const url = BASE_URL + '/payments/verify-premium/' + reference.reference
  const options = createOptions('GET')
  try {
      const response = await sendRequest(url, options)
      if (response.status !== 200) {
          const err = await response.json()
          console.log(err)
          return {
              status: response.status,
              data: null,
              error: err
          }
      }
     const resp = await response.json()
      return {
          status: response.status,
          data: data,
          error: null
      }
      
  } catch (err) {
      return {
          status: 500,
          data: null,
          error: err
      }
  }
  
}
