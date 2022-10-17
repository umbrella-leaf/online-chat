import dayjs from "dayjs";
import "dayjs/locale/zh-cn"
import relativeTime from "dayjs/plugin/relativeTime"
import isSameOrAfter from "dayjs/plugin/isSameOrAfter";

dayjs.locale("zh-cn");
dayjs.extend(relativeTime);
dayjs.extend(isSameOrAfter);

