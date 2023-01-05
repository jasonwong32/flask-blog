// 网站默认标题
export const websiteTitle = 'Flask Blog'

import axios from "axios";

const axiosInstance = axios.create()

axiosInstance.defaults.baseURL = 'http://127.0.0.1:5000'


export default axiosInstance
