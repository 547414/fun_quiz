import {UserListInfo, WebUserLoginDetail} from "@/api/webUserApi.ts";

export const getUserInfo = () => {
    const localStoreUserInfo = localStorage.getItem('unionUserInfo');
    const sessionStoreUserInfo = sessionStorage.getItem('unionUserInfo');
    let userInfoData: UserListInfo | null = null;
    let userList: UserListInfo[] = []
    if (localStoreUserInfo) {
        userList = JSON.parse(localStoreUserInfo)?.unionUserInfo?.userList
    }
    if (sessionStoreUserInfo) {
        userList = JSON.parse(sessionStoreUserInfo)?.unionUserInfo?.userList
    }
    for (const user of userList) {
        console.log('user ...')
        console.log(user)
        if (user.unionUserUserCategory === 'WEB_USER') {
            userInfoData = user
            break
        }
    }
    return userInfoData
}

export const getUnionUserInfo = () => {
    const localStoreUserInfo = localStorage.getItem('unionUserInfo');
    const sessionStoreUserInfo = sessionStorage.getItem('unionUserInfo');
    let unionUserInfo: WebUserLoginDetail = null
    if (localStoreUserInfo) {
        unionUserInfo = JSON.parse(localStoreUserInfo) as WebUserLoginDetail
    }
    if (sessionStoreUserInfo) {
        unionUserInfo = JSON.parse(sessionStoreUserInfo) as WebUserLoginDetail
    }
    return unionUserInfo
}

export const clearUserInfo = () => {
    localStorage.removeItem('userInfo');
    sessionStorage.removeItem('userInfo');
}
