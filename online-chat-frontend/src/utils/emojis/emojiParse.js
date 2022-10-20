import {defaultEmojisMap1} from "@/utils/emojis/default";

function getEmojiUrl(emotion) {
  emotion = emotion.split('[')[1].split(']')[0];
  if (defaultEmojisMap1.hasOwnProperty(emotion)) {
    let index = defaultEmojisMap1[emotion].match(/\d+/g)[0];
    return `<img src='https://res.wx.qq.com/mpres/htmledition/images/icon/emotion/${index}.gif' />`;
  }
  return `[${emotion}]`
}

export function emojiParse(message) {
  return message.replace(/\[\p{Unified_Ideograph}+\]/ug, getEmojiUrl);
}
