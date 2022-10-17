from enum import Enum


class UserState(Enum):
    # 用户验证状态
    authorized = 1
    unauthorized = 0


class FriendState(Enum):
    # 好友关系状态
    unaccepted = 0
    normal = 1
    pos_black = -1  # 主动拉黑
    neg_black = -2  # 被动拉黑


class MessageState(Enum):
    # 消息状态
    read = 1
    unread = 0


if __name__ == '__main__':
    print(UserState.authorized.value)