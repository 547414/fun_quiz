import {AxiosResponse} from "axios";

export const getFileNameFromHeaders = (headers: any) => {
    const contentDisposition = headers['content-disposition'];
    let fileName = null;

    if (contentDisposition) {
        // 支持 filename* 和 filename 的格式
        const filenameRegex = /filename\*=(?:UTF-8'')?([^;]+)|filename="?([^"]+)"?/i;
        const matches = contentDisposition.match(filenameRegex);

        if (matches) {
            // 优先使用 filename* 的值
            fileName = matches[1] ? decodeURIComponent(matches[1]) : matches[2];
        }
    }

    return fileName;
};

export const downloadFileByA = (res: AxiosResponse<Blob>) => {
    const url = window.URL.createObjectURL(res.data); // 创建 Blob URL
    const link = document.createElement('a'); // 创建 <a> 标签
    link.href = url;
    link.download = getFileNameFromHeaders(res.headers); // 设置文件名
    document.body.appendChild(link); // 添加到 DOM
    link.click(); // 触发点击事件下载文件
    link.remove(); // 下载完成后移除链接
    window.URL.revokeObjectURL(url); // 释放 Blob URL
}