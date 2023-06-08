from enum import Enum

class AnnouncementType(Enum):
    PICKED = 0
    DISCARDED = 1

class PublicAnnouncement:

    def __init__(self, sender, card, announcement_type: AnnouncementType):
        self.card = card
        self.sender = sender
        self.type = announcement_type

        print(f"Public Announcement: {self.sender.name} has {self.type.name} {(card.value, card.suit)}")
        
