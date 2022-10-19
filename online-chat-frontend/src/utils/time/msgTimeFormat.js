import dayjs from "dayjs";


function IsSameWeek(timeBefore, timeAfter) {
  let dayInWeek = timeAfter.day();
  if (dayInWeek === 0) dayInWeek = 7;
  // 计算今天凌晨时间
  const todayZeroTime = new Date(timeAfter.year(), timeAfter.month(), timeAfter.date());
  //本周开始的时间=今天凌晨时间-(今天是周几-1)，这里需要-1是因为凌晨已经刨去一天
  const weekStart = dayjs(todayZeroTime).subtract(dayInWeek - 1, 'day');
  //只要比这周的起始时间晚，就说明是本周内
  return timeBefore.isSameOrAfter(weekStart);
}


export function msgTimeFormat(time, chat_list=false) {
  const msg_time = dayjs(`${time}+8`);
  const now_time = dayjs();
  // 解析当前时间
  const curYear = now_time.year();
  const curMonth = now_time.month();
  const curDate = now_time.date();
  const duration = (hour) => {
    if (hour >= 0 && hour < 6) return '凌晨';
    if (hour < 12) return '上午';
    if (hour < 13) return '中午';
    if (hour < 18) return '下午';
    if (hour <= 23) return '晚上';
  }

  if (msg_time.year() === curYear) {
    if (msg_time.month() === curMonth) {
      const days_interval = curDate - msg_time.date();
      if (days_interval === 0) {
        const hour = msg_time.hour();
        const dur = duration(hour);
        return msg_time.format(`${dur}h:mm`);
      } else if (days_interval === 1) {
        const hour = msg_time.hour();
        const dur = duration(hour);
        if (chat_list) return '昨天';
        return msg_time.format(`昨天[&ensp;]${dur}h:mm`);
      } else if (IsSameWeek(msg_time, now_time)) {
        const week_str = ['周日', '周一', '周二', '周三', '周四', '周五', '周六'];
        const msg_week = msg_time.day();
        if (chat_list) return `${week_str[msg_week]}`;
        return msg_time.format(`${week_str[msg_week]}[&ensp;]HH:mm`);
      } else {
        const hour = msg_time.hour();
        const dur = duration(hour);
        if (chat_list) return msg_time.format(`M月D日`);
        return msg_time.format(`M月D日[&ensp;]${dur}HH:mm`);
      }
    } else {
      const hour = msg_time.hour();
      const dur = duration(hour);
      if (chat_list) return msg_time.format(`M月D日`);
      return msg_time.format(`M月D日[&ensp;]${dur}HH:mm`);
    }
  } else {
    if (chat_list) return msg_time.format(`YYYY年M月D日`);
    return msg_time.format(`YYYY年M月D日[&ensp;]HH:mm`)
  }
}
