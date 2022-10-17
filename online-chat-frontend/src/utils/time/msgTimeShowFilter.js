import {day} from "./index";
/**
 * 聊天时间格式化
 * 规则：
 *  1. 每五分钟为一个跨度
 *  2. 今天显示，小时:分钟，例如：11:12
 *  3. 昨天显示，昨天 小时:分钟 例如：昨天 11:12
 *  4. 一周内显示，星期几 小时:分钟 例如：星期四 11:12
 *  5. 日期差大于一周显示，年月日 小时:分钟 例如：2021年9月30日 11:12
 * @param currentMessageList 传入的当前会话数组
 * @param sort 传入数组排序：0-数组时间倒序；1-数组时间正序
 * @param type 五分钟规则区分：0-永远跟上一个显示的时间对比是否超5分钟 ；1-永远两条消息对比是否超5分钟
 * @returns {Array|null}
 */
export function msgTimeShowFilter(currentMessageList, sort, type) {
  // console.log('传入的会话数组', currentMessageList)
  const newMessageList = []
  const currentFilterList = currentMessageList.filter((item) => {
    return item.type !== 'showTime'
  })
  currentFilterList.forEach((item, index) => {
    let showTime;
    if (index === 0) {
      //第一条必显示时间
      showTime = day(`${item.time}+8`);
      newMessageList.push({
        payload: {
          text: showTime
        },
        type: 'showTime',//超五分钟显示时间-标识
        time: item.time
      })
      newMessageList.push(item)
    } else if (index <= currentFilterList.length - 1) {
      const current = currentFilterList[index].time
      let minutes
      const showTimeList = newMessageList.filter((item) => {
        return item.type === 'showTime'
      })
      const lastShowTime = showTimeList[showTimeList.length - 1].time//添加的时间且最后一条，用于对比
      if (type) {
        const prev = currentFilterList[index - 1].time
        minutes = (current - prev) / 60
      }
      if (!sort) {
        minutes = (current - lastShowTime) / 60
      } else {
        minutes = (lastShowTime - current) / 60
      }
      //超五分
      if (minutes > 5) {
        showTime = timestampFormat(date, '-', true)
        newMessageList.push({
          payload: {
            text: showTime
          },
          type: 'showTime',
          time: item.time
        })
        newMessageList.push(item)
      } else {
        newMessageList.push(item)
      }
    }
  })
  // console.log('最后得到的数组', newMessageList)
  return newMessageList
}
