const BASE_URL = 'http:/api/v1'

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