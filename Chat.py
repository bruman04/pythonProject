from datetime import datetime, timedelta
from shelve import open
from time import time_ns

# This is for chat, message, review, and feedback features:
from typing import List, Set


class Message:
    def __init__(
            self,
            sender_id: str = '',
            message: str = '',
            timestamp: int = 0,
            edited: bool = False,
            timeoffset: int = 8
    ):
        self.sender_id: str = sender_id
        self.message: str = message.strip()
        self.timestamp: int = timestamp if timestamp > 0 else time_ns()
        self.edited: bool = edited
        self.timeoffset: timedelta = timedelta(hours=timeoffset if -12 <= timeoffset <= 12 else 8)
        if not self.message.strip():
            self.delete()

    def id(self) -> str:
        return self.sender_id

    def msg(self) -> str:
        return self.message.strip()

    def time(self) -> int:
        return self.timestamp

    def timeFormat(self):
        return (datetime.utcfromtimestamp(self.timestamp / 1000000000) + self.timeoffset).strftime(
            "%d / %m / %Y  -  %H:%M:%S"
        )

    def isEdited(self) -> bool:
        return self.edited

    def timeDelta(self):
        return self.timeoffset

    def edit(self, new_message: str = ''):
        self.edited: bool = self.edited if self.message.strip() == new_message.strip() else True
        self.message: str = new_message.strip()
        if not self.message.strip():
            self.delete()
        return self

    def delete(self):
        self.sender_id: str = ''
        self.message: str = ''
        self.timestamp: int = 0
        self.edited: bool = False
        return self

    def __str__(self) -> str:
        return self.msg()


# This is for chat, message, review, and feedback features:

class Chat:
    def __init__(self, customer_id: str = '', vendor_id: str = '', db: str = "chat.db"):
        self.customer_id: str = customer_id
        self.vendor_id: str = vendor_id
        self.db: str = db.strip()
        self.chatKey: str = f"{customer_id}|{vendor_id}"

    def getLastMessageObject(self) -> Message:
        C: list[Message] = self.getChat()
        return C[-1] if C else Message().delete()

    def getUnreadMessagesCount(self, asVendor: bool) -> int:
        C: list[Message] = self.getChat()
        i: int = 0
        while C and C.pop(-1).sender_id == (self.customer_id if asVendor else self.vendor_id):
            i += 1
        return i

    def getChatsByID(self, _id: str) -> Set[str]:
        chats: set = set()
        chatdb = open(self.db, 'c')
        for k in chatdb:
            k = k.split('|')
            k = k[0], k[-1]
            if k[0] == _id:
                chats.add(k[-1])
            elif k[-1] == _id:
                chats.add(k[0])
        chatdb.close()
        return chats

    def getChat(self) -> List[Message]:
        chatdb = open(self.db, 'c')
        if self.chatKey in chatdb:
            chat = chatdb[self.chatKey]
        else:
            chat = chatdb[self.chatKey] = []
        chatdb.close()
        return chat

    def setChat(self, chat: List[Message]) -> bool:
        chatdb = open(self.db, 'c')
        try:
            chatdb[self.chatKey] = chat
        except:
            return False
        finally:
            chatdb.close()
        return True

    def delChat(self) -> bool:
        chatdb = open(self.db, 'c')
        try:
            chatdb.pop(self.chatKey)
            try:
                del chatdb[self.chatKey]
            except:
                pass
            del self
        except:
            return False
        finally:
            chatdb.close()
        return True

    def appendMultiChat(self, messageObjects: List[Message]) -> bool:
        return self.setChat(self.getChat() + [m for m in messageObjects if m.msg().strip()])

    def appendChatMessage(self, asVendor: bool, message: str, utcTimezone: int = 8) -> bool:
        if message.strip():
            c: list[Message] = self.getChat()
            c.append(Message(
                sender_id=self.vendor_id if asVendor else self.customer_id,
                message=message.strip(),
                timeoffset=utcTimezone
            ))
            return self.setChat(c)
        return False

    def editChatMessage(self, message_index: int, new_message: str) -> bool:
        if new_message.strip():
            c: list[Message] = self.getChat()
            try:
                c[message_index] = c[message_index].edit(new_message.strip())
            except IndexError:
                return False
            return self.setChat(c)
        return self.delChatMessage(message_index)

    def delChatMessage(self, message_index: int) -> bool:
        C: list[Message] = self.getChat()
        try:
            del C[message_index]
        except IndexError:
            return False
        return self.setChat(C)

# This is for chat, message, review, and feedback features.
