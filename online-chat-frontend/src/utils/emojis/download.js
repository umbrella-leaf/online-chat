export const downloadFile = (fileUrl, fileName) =>  {
  const a = document.createElement('a');
   // 完整的url则直接使用
  // 这里是将url转成blob地址，
  fetch(fileUrl, {mode: "cors"})  // 跨域时不报错
    .then(res => res.blob())
    .then(blob => { // 将链接地址字符内容转变成blob地址
      a.href = URL.createObjectURL(blob);
      a.download = fileName; // 下载文件的名字
      document.body.appendChild(a);
      a.click();
      //在资源下载完成后 清除 占用的缓存资源
      window.URL.revokeObjectURL(a.href);
      document.body.removeChild(a);
    })
}
