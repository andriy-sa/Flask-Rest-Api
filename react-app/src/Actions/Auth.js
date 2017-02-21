export const SET_USER = 'SET_USER'

export function setUser(activeUser) {
  return {
    type: SET_USER,
    activeUser
  }
}