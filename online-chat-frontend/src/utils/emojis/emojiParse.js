import {WeChatEmojisMap, QQEmojisMap} from "@/utils/emojis/default";

function getWeChatEmojiUrl(emotion) {
  emotion = emotion.split('[')[1].split(']')[0];
  if (WeChatEmojisMap.hasOwnProperty(emotion)) {
    let index = WeChatEmojisMap[emotion].match(/\d+/g)[0];
    return `<img src='https://res.wx.qq.com/mpres/htmledition/images/icon/emotion/${index}.gif' />`;
  }
  return `[${emotion}]`;
}

function getQQEmojiUrl(emotion) {
  emotion = emotion.split('<')[1].split('>')[0];
  if (QQEmojisMap.hasOwnProperty(emotion)) {
    let index = QQEmojisMap[emotion].match(/\d+/g)[0];
    return `<img src='https://www.emojiall.com/img/platform/qq/${index}@2x.gif' />`;
  }
  return `[${emotion}]`;
}

// 将消息中的['表情名']转化为真正的表情图片
export function emojiParse(message) {
  return message
    .replace(/\[\p{Unified_Ideograph}+\]/ug, getWeChatEmojiUrl).replace(/<\p{Unified_Ideograph}+>/ug, getQQEmojiUrl);
}
