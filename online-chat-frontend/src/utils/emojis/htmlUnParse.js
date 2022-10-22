import {QQEmojisMap, WeChatEmojisMap} from "@/utils/emojis/default";

function getWeChatEmojiName(emoji) {
  const emoji_no = emoji.match(/\d+/g)[0];
  for (const emoji_name in WeChatEmojisMap) {
    if (WeChatEmojisMap[emoji_name].includes(emoji_no)) {
      return `[${emoji_name}]`
    }
  }
  return ``
}

function getQQEmojiName(emoji) {
  const emoji_no = emoji.match(/\d+/g)[0];
  for (const emoji_name in QQEmojisMap) {
    if (QQEmojisMap[emoji_name].includes(emoji_no)) {
      return `[${emoji_name}]`
    }
  }
  return ``
}


// html格式消息中的表情转化为['表情名']格式
export function htmlUnParse(html) {
  return html.replace(/<(?!img).*?>/gi, '')
    .replace(/<(?=img).*?wx.*?>/gi, getWeChatEmojiName)
    .replace(/<(?=img).*?qq.*?>/gi, getQQEmojiName);
}
