from enum import Enum


class AnnouncementType(Enum):
    PICKED = 0
    DISCARDED = 1
    KEMPS = 2


class PublicAnnouncement:
    """ Class that records information for a public announcement """
    def __init__(self, sender, card, announcement_type: AnnouncementType):
        # card is the card involved in the public announcement (that was picked, discarded or used for Kemps)
        self.card = card
        # sender is the agent that made the move
        self.sender = sender
        # type is the type of the public announcement (a card can be picked, discarded or used for Kemps)
        self.type = announcement_type

        print(f"Public Announcement: {self.sender.name} has {self.type.name} {(card.value, card.suit)}")


def make_announcements(announcements, players):
    """
    Send the announcement to all players other than the sender
    :param announcements: a list of announcements
    :param players: a list of player identifiers
    :return: None
    """
    for announcement in announcements:
        sender = announcement.sender
        for player in players:
            if player.name != sender.name:
                # print(f"KB of {player.name} before announcement({announcement.sender.name} has {announcement.type.name} {(announcement.card.value, announcement.card.suit)}): {player.kb}")
                # print(f"Player {player.name} recieved announcement: {announcement.sender.name} has {announcement.type.name} {(announcement.card.value, announcement.card.suit)}")
                player.recieve_announcement(announcement)
                # print(f"KB of {player.name} after announcement({announcement.sender.name} has {announcement.type.name} {(announcement.card.value, announcement.card.suit)}): {player.kb}")
