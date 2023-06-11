from enum import Enum

class AnnouncementType(Enum):
    PICKED = 0
    DISCARDED = 1
    KEMPS = 2

class PublicAnnouncement:

    def __init__(self, sender, card, announcement_type: AnnouncementType):
        self.card = card
        self.sender = sender
        self.type = announcement_type

        print(f"Public Announcement: {self.sender.name} has {self.type.name} {(card.value, card.suit)}")


def make_announcements(announcements, players):
    for announcement in announcements:
        sender = announcement.sender
        for player in players:
            if player.name != sender.name:
                print(f"KB of {player.name} before announcement({announcement.sender.name} has {announcement.type.name} {(announcement.card.value, announcement.card.suit)}): {player.kb}")
                print(f"Player {player.name} recieved announcement: {announcement.sender.name} has {announcement.type.name} {(announcement.card.value, announcement.card.suit)}")
                player.recieve_announcement(announcement)
                print(f"KB of {player.name} after announcement({announcement.sender.name} has {announcement.type.name} {(announcement.card.value, announcement.card.suit)}): {player.kb}")
